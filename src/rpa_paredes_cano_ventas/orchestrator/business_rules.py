from dataclasses import dataclass
from rpa_paredes_cano_ventas.apps.imports import (
    ImportMainWindow,
    ImportLoginWindow,
    VasicontLauncher,
)
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.utils.credentials import CredentialManager
from rpa_paredes_cano_ventas.types import DataCSV
from pathlib import Path
from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro
from typing import Sequence, Optional
from rpa_paredes_cano_ventas.processor.series import SeriesSincronizador


# import_app = ImportPlatform()
# aconsys_app = AconsysPlatform()
@dataclass(frozen=True, slots=True)
class BusinessRulesWithApps:
    @staticmethod
    def execute(data_csv: DataCSV):
        credential = CredentialManager.get_credential("IMPORTACIONES")
        VasicontLauncher(routes.IMPORTACION_PATH).open()
        main_imports = ImportLoginWindow(routes.IMPORTACION_PATH).login(
            username=credential.username, password=credential.password
        )
        # Solo obtenemos el archivo si hubo errores/exportación
        excel_file: Optional[Path] = None
        excel_file = procesar_carga_y_exportar_errores(main_imports, data_csv)
        errores_raw: tuple[RegistroMaestro, ...] = ()

        if not excel_file:
            print("No se generó archivo de exportación. Proceso finalizado.")
            return

        # 3. Gestión de Diferencias (Aconsys)
        errores_raw = GetRegistroMaestroFromExcel.execute(
            file=excel_file, mode="simple"
        )
        series_ref = GetRegistroMaestroFromExcel.execute(
            file=main_imports.download_series, mode="FULL"
        )
        # 2. Aplicar el patrón
        sincronizador = SeriesSincronizador(series_ref)
        nuevas_series = sincronizador.identify_new_series(errores_raw, series_ref)

        if nuevas_series:
            # 4. Registro en ambas plataformas
            credential = CredentialManager.get_credential("ACONSYS")
            aconsys_files = aconsys_app.download_reports()
            aconsys_app.register_series(new_series)
            import_app.register_series(new_series)


from pathlib import Path
from typing import Sequence, Literal
import pandas as pd
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetRegistroMaestroFromExcel:
    # Definimos los esquemas de columnas como constantes de clase
    SCHEMAS = {
        "simple": {"Serie": "serie", "Sucursal": "sucursal"},
        "full": {
            "Serie": "serie",
            "C.C.": "centro_costo",
            "Descripción": "descripcion_cc",
            "Sucursal": "sucursal",
            "T.Op.": "tipo_oper",
            "Descripción.1": "descripcion_oper",
            "Cta.Cte.": "cuenta_corriente",
            "Descripción.2": "descripcion_cta",
        },
    }

    @classmethod
    def execute(
        cls, file: Path, mode: Literal["simple", "full"] = "full"
    ) -> tuple[RegistroMaestro, ...]:
        """
        Un solo punto de entrada para cualquier tipo de extracción.
        """
        mappings = cls.SCHEMAS.get(mode, cls.SCHEMAS["full"])

        # Leemos el archivo
        df = pd.read_excel(file, engine="calamine", header=0, dtype=str)

        # Seleccionamos solo las columnas que existen en nuestro mapeo y renombramos
        # El uso de .intersection asegura que no explote si falta una columna opcional
        cols_to_use = [c for c in df.columns if c in mappings]

        df = df[cols_to_use].rename(columns=mappings)

        return tuple(RegistroMaestro(**data) for data in df.to_dict(orient="records"))


def procesar_carga_y_exportar_errores(
    main_imports: ImportMainWindow, data_csv: DataCSV
) -> Optional[Path]:
    """
    Coordina la carga de archivos y devuelve la ruta del Excel de errores
    solo si el proceso de exportación fue exitoso.
    """
    importacion = main_imports.sales_imports
    importacion.period(data_csv.period)
    importacion.start

    for file in data_csv.files:
        importacion.select_file(file)
        importacion.upload

    excel_file: Optional[Path] = None
    # Solo intentamos exportar si la plataforma indica que hay algo que procesar
    if importacion.process:
        # Asumimos que el primer archivo nos da la ruta base
        excel_file = importacion.export(data_csv.save_dir, data_csv.period)

    importacion.exit

    # Verificamos que el archivo realmente exista antes de devolverlo
    if excel_file and excel_file.exists():
        return excel_file

    return None

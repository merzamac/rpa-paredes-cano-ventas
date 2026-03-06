from rpa_paredes_cano_ventas.apps.imports import (
    ImportMainWindow,
    ImportLoginWindow,
    VasicontLauncher,
)
from rpa_paredes_cano_ventas.apps.aconsys import AconsyMainWindow, AconsyLoginWindow
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.utils.credentials import CredentialManager
from rpa_paredes_cano_ventas.types import DataCSV
from pathlib import Path
from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro
from typing import Optional, Literal
from rpa_paredes_cano_ventas.processor.series import SeriesSincronizador
from pathlib import Path
import pandas as pd
from dataclasses import dataclass


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
        excel_file = main_imports.import_files(data_csv)
        # excel_file = procesar_carga_y_exportar_errores(main_imports, data_csv)
        errores_raw: list[RegistroMaestro]

        if not excel_file:
            print("No se generó archivo de exportación. Proceso finalizado.")
            return

        # . Gestión de Diferencias (Aconsys)
        errores_raw = GetRegistroMaestroFromExcel.execute(
            file=excel_file, mode="simple"
        )
        name = f"series{data_csv.period.month:02d}{str(data_csv.period.year)[-2:]}"
        series_ref = GetRegistroMaestroFromExcel.execute(
            file=main_imports.download_series(data_csv.save_dir, name), mode="FULL"
        )
        #  Aplicar el patrón
        sincronizador = SeriesSincronizador(series_ref)
        new_series = sincronizador.identify_new_series(errores_raw, series_ref)

        if new_series:

            # Registro en ambas plataformas
            credential = CredentialManager.get_credential("ACONSYS")
            main_aconsys: AconsyMainWindow = AconsyLoginWindow(
                routes.ACONSYS_PATH
            ).login(username=credential.username, password=credential.password)
            main_aconsys.change_work_period(data_csv.period)
            pdf_name = "centros_costos"
            cost_centers: dict[str, str] = main_aconsys.get_cost_centers(
                data_csv.save_dir, pdf_name
            )
            last_account_number = main_aconsys.last_account_number

            errors = sincronizador.update_news(
                last_account_number, cost_centers, new_series
            )

            if errors:
                # dejar notificacion de errores
                return
            main_aconsys.register_accounts(new_series)

        series = new_series + series_ref
        series_updated = sincronizador.create_series(data_csv.save_dir, name, series)

        main_imports.upload_series(series_updated)


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
    ) -> list[RegistroMaestro]:
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

        return [RegistroMaestro(**data) for data in df.to_dict(orient="records")]

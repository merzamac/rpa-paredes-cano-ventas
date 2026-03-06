from numpy._core.defchararray import zfill
from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro
from pathlib import Path
from pandas import DataFrame
from thefuzz.process import extractOne


class SeriesSincronizador:
    """Encapsula la lógica de comparación y enriquecimiento de series."""

    def __init__(self, maestro_plataforma: tuple[RegistroMaestro]):
        # Indexamos para búsquedas O(1)
        self.mapa_series: dict[str, RegistroMaestro] = {
            r.serie: r for r in maestro_plataforma
        }
        self.mapa_sucursales: dict[str, RegistroMaestro] = {
            r.sucursal: r for r in maestro_plataforma
        }

    def identify_new_series(
        self,
        errores: list[RegistroMaestro],
        maestro_plataforma: list[RegistroMaestro],
    ) -> list[RegistroMaestro]:
        """Separa errores en: (coincidencias_enriquecidas, nuevas_series)."""
        nuevos: list[RegistroMaestro] = []
        for_test: list[RegistroMaestro] = []
        for err in errores:
            # Lógica de coincidencia
            series_exists = self.mapa_series.get(err.serie)

            if series_exists:
                sucursal_exists = self.mapa_sucursales.get(err.sucursal)
                if sucursal_exists:
                    err.centro_costo = sucursal_exists.centro_costo
                    err.descripcion_cc = sucursal_exists.descripcion_cc
                    # tipo de operacion es estatico, 20
                    err.descripcion_oper = sucursal_exists.descripcion_oper
                    err.cuenta_corriente = sucursal_exists.cuenta_corriente
                    err.descripcion_cta = sucursal_exists.descripcion_cta
                    maestro_plataforma.append(err)
                    for_test.append(err)
            else:
                nuevos.append(err)
        Path("modificadas_al_instante.txt").write_text(str(for_test), encoding="utf-8")
        return nuevos

    @staticmethod
    def create_series(
        output_dir: Path, name: str, maestro_plataforma: list[RegistroMaestro]
    ) -> Path:

        data = [tuple(registro) for registro in maestro_plataforma]
        columns = [
            "Serie",
            "C.C.",
            "Descripción",
            "Sucursal",
            "T.Op.",
            "Descripción",
            "Cta.Cte.",
            "Descripción",
        ]
        df = DataFrame(data, columns=columns)
        df.index = range(1, len(df) + 1)
        df.index.name = "Sec."
        file = output_dir / f"{name}.xlsx"

        df.to_excel(file, sheet_name="Hoja1")
        return file

    @staticmethod
    def update_news(
        last_account_number: int,
        cost_centers: dict,  # Estructura: {"NOMBRE": "CODIGO"}
        new_series: list,
    ) -> list:

        def normalize(sucursal: str) -> str:
            mapa = {
                "PLZ": "PLAZA",
                "M.A.": "MALL AVENTURA",
                "M.A": "MALL AVENTURA",
                "C.CIVICO": "CENTRO CIVICO",
                "CDR": "CUADRA",
                "CDRA": "CUADRA",
                "PURUCHUC": "PURUCHUCO",
                "V.E.S": "VILLA EL SALVADOR",
                "AV": "AVENIDA",
                "AV.": "AVENIDA",
            }
            # Normalizamos a mayúsculas para evitar fallos por "Av" vs "AV"
            palabras = sucursal.upper().split()
            norm = [mapa.get(p, p) for p in palabras]
            return " ".join(norm)

        errors = []

        for series in new_series:
            sucursal_norm = normalize(series.sucursal)

            # Buscamos sobre las LLAVES (nombres de sucursales)
            coincidence, score = extractOne(sucursal_norm, cost_centers.keys())

            if score > 95:
                # Ahora sí, cost_centers[coincidence] nos da el código "001"
                number_cc = cost_centers[coincidence]

                # Modificamos el objeto original (los cambios persisten en new_series)
                series.centro_costo = number_cc
                last_account_number += 1
                series.cuenta_corriente = f"{last_account_number:011d}"
                series.descripcion_cc = f"TICKETS VARIOS - {coincidence}"
            else:
                # Si no hay match suficiente, lo mandamos a la lista de pendientes
                errors.append(series)

        return errors

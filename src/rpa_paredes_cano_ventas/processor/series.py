from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro


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
        errores: tuple[RegistroMaestro],
        maestro_plataforma: list[RegistroMaestro],
    ) -> Tuple[RegistroMaestro]:
        """Separa errores en: (coincidencias_enriquecidas, nuevas_series)."""
        nuevos: list[RegistroMaestro] = []

        for err in errores:
            # Lógica de coincidencia
            maestro = self.mapa_series.get(err.serie) or self.mapa_sucursales.get(
                err.sucursal
            )

            if maestro:
                err.centro_costo = maestro.centro_costo
                err.descripcion_cc = maestro.descripcion_cc
                maestro_plataforma.append(err)
            else:
                nuevos.append(err)

        return tuple(nuevos)

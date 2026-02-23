from dataclasses import dataclass


# import_app = ImportPlatform()
# aconsys_app = AconsysPlatform()
@dataclass(frozen=True, slots=True)
class BusinessRulesWithApps:
    @staticmethod
    def execute(csv_outputs):
        # 2. Carga y Verificación
        import_results = import_app.upload_csvs(csv_outputs)

        if import_results.has_no_details():
            print("Proceso finalizado con éxito.")
            return

        # 3. Gestión de Diferencias (Aconsys)
        aconsys_files = aconsys_app.download_reports()
        new_series = file_service.identify_new_series(import_results, aconsys_files)

        if new_series:
            # 4. Registro en ambas plataformas
            aconsys_app.register_series(new_series)
            import_app.register_series(new_series)

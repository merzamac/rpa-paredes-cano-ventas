from dataclasses import dataclass
from rpa_paredes_cano_ventas.apps.imports import ImportMainWindow,ImportLoginWindow,VasicontLauncher
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.utils.credentials import CredentialManager
from rpa_paredes_cano_ventas.types import DAtaCSV
from pathlib import Path
from pandas import read_excel, DataFrame
from rpa_paredes_cano_ventas.models.registro_maestro import RegistroMaestro
# import_app = ImportPlatform()
# aconsys_app = AconsysPlatform()
@dataclass(frozen=True, slots=True)
class BusinessRulesWithApps:
    @staticmethod
    def execute(data_csv:DAtaCSV):
        # 2. Carga y Verificación
        credential = CredentialManager.get_credential("IMPORTACIONES")
        VasicontLauncher(routes.IMPORTACION_PATH).open()
        main_window = ImportLoginWindow(routes.IMPORTACION_PATH).login(
        username=credential.username, password=credential.password)   

        importacion = main_window.sales_imports
        importacion.period(data_csv.period)
        importacion.start
        
        for file in data_csv.files:
            importacion.select_file(file)
            importacion.upload

        import_results:dict={}
        if importacion.process:
            excel_file = importacion.export(file.parent,data_csv.period)
            centros_costos_export = GetDataFromExcel.execute(excel_file)
            #import_results = import_app.upload_csvs(csv_outputs)
        importacion.exit
        

        # if import_results.has_no_details():
        #     print("Proceso finalizado con éxito.")
        #     return

        # # 3. Gestión de Diferencias (Aconsys)
        # aconsys_files = aconsys_app.download_reports()
        # new_series = file_service.identify_new_series(import_results, aconsys_files)

        # if new_series:
        #     # 4. Registro en ambas plataformas
        #     aconsys_app.register_series(new_series)
        #     import_app.register_series(new_series)



    # main_window.open_menu("Procesos", "Importación Ventas", 5)
    #sleep(5)
    # cuenta_corriente(main_window._window)
    # main_window.open_menu_mante("Mantimiento", "Series por Centro de Costo", 2)
    
    
    # resultado_import = open_menu_option(
    #     main_window._window,
    #     menu_name="Procesos",
    #     option_name="Importación Ventas",
    #     pasos_derecha=5,
    #     _date=_date,
    #     files_to_import=archivos_csv
    # )

@dataclass(frozen=True, slots=True)
class GetDataFromExcel:
    def execute(file:Path):
        df_info = read_excel(file, engine="calamine",header=0,usecols=["Serie", "Sucursal"], dtype="str")
        registros_dict = df_info.rename(columns={
        "Serie": "serie", 
        "Sucursal": "sucursal"
        }).to_dict(orient='records')
        return tuple(RegistroMaestro(**data) for data in registros_dict)
    
    def exported_file(file):
        df_info = read_excel(file, engine="calamine",header=0,usecols=["Serie", "Sucursal"], dtype="str")
        registros_dict = df_info.rename(columns={
        "Serie": "serie", 
        "Sucursal": "sucursal"
        }).to_dict(orient='records')
        return tuple(RegistroMaestro(**data) for data in registros_dict)


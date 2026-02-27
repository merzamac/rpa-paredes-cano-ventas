from pathlib import Path
from collections import defaultdict
from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro
from rpa_paredes_cano_ventas.orchestrator.business_rules import (
    GetRegistroMaestroFromExcel,
)
from PIL import Image
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
from re import Match, search, split, findall
from typing import cast
from rpa_paredes_cano_ventas.apps.imports import (
    ImportLoginWindow,
    VasicontLauncher,
)
from rpa_paredes_cano_ventas.ocr_processor.parser import DataParser
from rpa_paredes_cano_ventas.ocr_processor import PyOcr, TesseractEngine
from rpa_paredes_cano_ventas.ocr_processor.helpers import img_to_ndarry, take_screenshot
from time import sleep
from rpa_paredes_cano_ventas.types import DocumentType
from rpa_paredes_cano_ventas.apps.aconsys import AconsyLoginWindow,AconsyMainWindow
from rpa_paredes_cano_ventas.utils.credentials import CredentialManager
from rpa_paredes_cano_ventas import routes
from rpa_paredes_cano_ventas.utils.pdf_reader import pdf_process
def natural_sort_key(registro: RegistroMaestro):
    """
    Divide la serie en partes de texto y números enteros.
    Ejemplo: 'F005' -> ['F', 5]
    """
    # Buscamos grupos de letras y grupos de números
    parts = split(r"(\+d)", registro.serie)

    # Convertimos a entero lo que sea un número, el resto se queda en minúsculas
    return [int(text) if text.isdigit() else text.lower() for text in parts]


def test_series(excel_errores: Path):

    result = GetRegistroMaestroFromExcel.execute(file=excel_errores, mode="simple")

    assert result


def test_get_series(excel_series: Path):
    credential = CredentialManager.get_credential("IMPORTACIONES")
    VasicontLauncher(routes.IMPORTACION_PATH).open()
    main_imports = ImportLoginWindow(routes.IMPORTACION_PATH).login(
            username=credential.username, password=credential.password
    )
    file_name = "series"
    file = main_imports.download_series(routes.OUTPUT_DIR,file_name)
    result = GetRegistroMaestroFromExcel.execute(file=file, mode="FULL")

def test_subir_series(excel_series: Path):
    credential = CredentialManager.get_credential("IMPORTACIONES")
    VasicontLauncher(routes.IMPORTACION_PATH).open()
    main_imports = ImportLoginWindow(routes.IMPORTACION_PATH).login(
            username=credential.username, password=credential.password
    )
    file_name = "series"
    main_imports.upload_series(excel_series)
    assert excel_series

def test_get_cost_center():
    credential = CredentialManager.get_credential("ACONSYS")
    main_aconsys = AconsyLoginWindow(routes.ACONSYS_PATH).login(
            username=credential.username, password=credential.password
    )
    cost_centers = main_aconsys.centros_de_costos
    file = "centros"
    file = cost_centers.exportar_centros_costos(routes.OUTPUT_DIR,file)
    result = pdf_process(file)
    assert result
  
    #file = main_aconsys.download_cost_centers()
    
def test_finding(excel_series: Path, excel_errores: Path):
    series = GetRegistroMaestroFromExcel.execute(file=excel_series, mode="FULL")
    errores = GetRegistroMaestroFromExcel.execute(file=excel_errores, mode="simple")
    # 1. Creamos universos de búsqueda rápida
    mapa_series = {r.serie: r for r in series}
    mapa_sucursales = {r.sucursal: r for r in series}

    errores_con_coincidencia = []
    errores_limpios = []

    # 2. Clasificamos
    for err in errores:
        # Buscamos el registro original en nuestros mapas
        coincidencia_serie = mapa_series.get(err.serie)
        coincidencia_sucursal = mapa_sucursales.get(err.sucursal)
        # ¿La serie existe en el set A O la sucursal existe en el set A?
        if coincidencia_serie or coincidencia_sucursal:
            origen = coincidencia_serie or coincidencia_sucursal
            err.centro_costo = origen.centro_costo
            err.descripcion_cc = origen.descripcion_cc
            errores_con_coincidencia.append(err)
        else:
            errores_limpios.append(err)


    series_por_tipo = defaultdict(list)

    for registro in series:
        series_por_tipo[registro.tipo_serie].append(registro)

    # Ordenamos cada grupo internamente
    for tipo in series_por_tipo:
        series_por_tipo[tipo].sort(key=natural_sort_key)
    assert errores_con_coincidencia

def test_cuenta_corrientes(a_type:str, code:str):
    credential = CredentialManager.get_credential("ACONSYS")
    main_aconsys = AconsyLoginWindow(routes.ACONSYS_PATH).login(
            username=credential.username, password=credential.password
    )
    
    cuentas_corrientes = main_aconsys.cuentas_corrientes
    cuentas_corrientes.start
    cuentas_corrientes.clients
    cuentas_corrientes.provider
    # cuentas_corrientes.account_code(code)
    # cuentas_corrientes.ruc()
    # cuentas_corrientes.description(code)
    cuentas_corrientes.document_type(DocumentType.OTROS)
    cuentas_corrientes.close
    
def test_get_last_cc(code:str):
    credential = CredentialManager.get_credential("ACONSYS")
    main_aconsys = AconsyLoginWindow(routes.ACONSYS_PATH).login(
            username=credential.username, password=credential.password
    )
    
    cuentas_corrientes = main_aconsys.cuentas_corrientes
    cuentas_corrientes.start
    cuentas_corrientes.clients
    cuentas_corrientes.provider
    cuentas_corrientes.account_code(code)
    cuentas_corrientes.ruc()
    cuentas_corrientes.description("TICKETS")
    cuentas_corrientes.search
    cuentas_corrientes.scroll_until_end
    tesseract = TesseractEngine(routes.TESSERACT)
    ocr_tool = PyOcr(engine=tesseract)
    raw_text = ocr_tool.process(
        image_source=img_to_ndarry(take_screenshot(cuentas_corrientes.content)),
    )
    accounts, companies = DataParser.clean_text(raw_text)
    accounts_companies = DataParser.format_results(accounts, companies)
    last_account_number = max(int(acc) for acc in accounts)
    assert last_account_number

def test_ocr():
    raw_text = Path("cc.txt").read_text(encoding="utf-8")
    # Aplicamos Regex
    accounts, companies = DataParser.clean_text(raw_text)
    data_final = DataParser.format_results(accounts, companies)
    last_account_number = max(int(acc) for acc in accounts)
    assert raw_text

    
    

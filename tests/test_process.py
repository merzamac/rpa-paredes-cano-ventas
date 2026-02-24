from pathlib import Path
from collections import defaultdict
from rpa_paredes_cano_ventas.processor.registro_maestro import RegistroMaestro
from rpa_paredes_cano_ventas.orchestrator.business_rules import (
    GetRegistroMaestroFromExcel,
)
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
from re import Match, search, split, findall
from typing import cast


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


def test_series_export(excel_series: Path):

    result = GetRegistroMaestroFromExcel.execute(file=excel_series, mode="FULL")

    assert result


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


import re
from typing import Dict, List
from pdfminer.high_level import extract_text


import re
from typing import Dict, List
from pdfminer.high_level import extract_pages, extract_text


def es_ruido(linea: str) -> bool:
    """Reglas de limpieza para el reporte de ACONSYS."""
    PALABRAS_CONTROL = {
        "Código",
        "Descripción",
        "Página",
        "Fecha",
        "Hora",
        "Inf.",
        "BIJOU",
        "ACONSYS",
    }
    FLAGS_ESTADO = {"S", "N", "A", "I"}
    if linea in PALABRAS_CONTROL or linea in FLAGS_ESTADO:
        return True
    if linea.isdigit():
        return True
    if re.match(r"\d{2}[/:]\d{2}[/:]", linea):
        return True
    return False


def test_extraer_maestro_pdf_multipagina(pdf_file: str) -> Dict[str, str]:
    # Diccionario final unificado
    centros_costos = {}

    # Iteramos por cada página (page_numbers empieza en 0)
    # page_numbers=None procesa todas las páginas
    for page_layout in extract_pages(pdf_file):
        page_no = page_layout.pageid
        # Extraemos el texto solo de esta página
        texto_pagina = extract_text(pdf_file, page_numbers=[page_no - 1])

        # 1. Códigos de la página
        codigos = re.findall(r"(?m)^\d{4}$", texto_pagina)

        # 2. Descripciones de la página
        descripciones = []
        en_zona = False
        for linea in (l.strip() for l in texto_pagina.split("\n") if l.strip()):
            if "Descripción" in linea:
                en_zona = True
                continue
            if "Página :" in linea:
                en_zona = False
                continue

            if en_zona and not es_ruido(linea):
                descripciones.append(linea)

        # 3. Validación de integridad POR PÁGINA
        if len(codigos) != len(descripciones):
            raise ValueError(
                f"Error en PÁGINA {page_no}: {len(codigos)} códigos vs {len(descripciones)} descripciones. "
                f"No se puede continuar para evitar desalineación de datos."
            )

        # 4. Unir al maestro total
        centros_costos.update(dict(zip(codigos, descripciones)))

    return centros_costos

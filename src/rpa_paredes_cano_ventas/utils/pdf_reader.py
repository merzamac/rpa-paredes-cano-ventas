from re import match,findall
from pdfminer.high_level import extract_pages, extract_text
from pathlib import Path
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
    if match(r"\d{2}[/:]\d{2}[/:]", linea):
        return True
    return False


def pdf_process(pdf_file: Path) -> dict[str, str]:
    # Diccionario final unificado
    centros_costos = {}

    # Iteramos por cada página (page_numbers empieza en 0)
    # page_numbers=None procesa todas las páginas
    for page_layout in extract_pages(pdf_file):
        page_no = page_layout.pageid
        # Extraemos el texto solo de esta página
        texto_pagina = extract_text(pdf_file, page_numbers=[page_no - 1])

        # 1. Códigos de la página
        codigos = findall(r"(?m)^\d{4}$", texto_pagina)

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

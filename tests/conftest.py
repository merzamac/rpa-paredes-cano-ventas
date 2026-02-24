from pytest import fixture
from rpa_paredes_cano_ventas import routes
from pathlib import Path


@fixture(scope="session")
def input_dir() -> Path:
    return routes.INPUT_DIR


@fixture(scope="session")
def output_dir() -> Path:
    return routes.OUTPUT_DIR


@fixture(scope="session")
def excel_errores() -> Path:
    files = routes.OUTPUT_DIR.rglob(pattern="*.xlsx", case_sensitive=True)

    excel = tuple(file for file in files if file.stem.startswith("errores"))
    return excel[0] or Path()


@fixture(scope="session")
def pdf_file() -> Path:
    files = tuple(routes.OUTPUT_DIR.rglob(pattern="*.pdf", case_sensitive=True))

    return files[0] or Path()


@fixture(scope="session")
def excel_series() -> Path:
    files = routes.OUTPUT_DIR.rglob(pattern="*.xlsx", case_sensitive=True)

    excel = tuple(file for file in files if file.stem.startswith("series"))
    return excel[0] or Path()

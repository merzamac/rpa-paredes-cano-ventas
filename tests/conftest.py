from pytest import fixture
from rpa_paredes_cano_ventas import routes
from pathlib import Path


@fixture(scope="session")
def input_dir() -> Path:
    return routes.INPUT_DIR


@fixture(scope="session")
def output_dir() -> Path:
    return routes.OUTPUT_DIR

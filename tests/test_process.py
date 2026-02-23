from pathlib import Path
from rpa_paredes_cano_ventas.orchestrator.business_rules import GetDataFromExcel
def test_series(excel_errores:Path):

    result = GetDataFromExcel.execute(excel_errores)

    assert result

def test_series_export(excel_errores:Path):

    pass

    


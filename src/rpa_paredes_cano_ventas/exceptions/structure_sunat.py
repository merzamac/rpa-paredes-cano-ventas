class PLEStructureError(Exception):
    """Clase base para excepciones del PLE."""

    pass


class DifferentTemplateLengthError(PLEStructureError):
    """Se lanza cuando el número de columnas no coincide con el esperado."""

    def __init__(self, actual, expected):
        self.message = (
            f"Column count mismatch: Excel has {actual}, expected {expected}."
        )
        super().__init__(self.message)


class ColumnMismatchTemplateError(PLEStructureError):
    """Se lanza cuando el nombre o posición de una columna no coincide."""

    def __init__(self, actual, expected):
        self.message = f"Found '{actual}', expected '{expected}'."
        super().__init__(self.message)


class SheetNameNotFoundError(PLEStructureError):
    """Se lanza cuando la hoja no se encuentra en el archivo Excel."""

    def __init__(self, sheet_name, available_sheetnames):
        self.message = (
            f"Sheetname '{sheet_name}' not found in the Excel file. "
            f"Available sheetnames: {available_sheetnames}"
        )
        super().__init__(self.message)


class PositionSheetNameNotZeroError(PLEStructureError):
    """Se lanza cuando el nombre de la hoja 'SUNAT' no se encuentra en la primera posicion"""

    def __init__(self, sheet_name, available_sheetnames):
        self.message = f"Sheetnames order is incorrect. Sheetname '{sheet_name}' should be the first one, available sheetnames: {available_sheetnames}"
        super().__init__(self.message)

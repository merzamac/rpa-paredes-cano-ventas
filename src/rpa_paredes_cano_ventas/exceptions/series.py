class SeriesValidation(Exception):
    """Base exception for the file processing module."""

    def __init__(self, name: str):
        super().__init__(name)


class SeriesEmptyError(SeriesValidation):
    """Se lanza cuando la serie es vacia."""

    pass


class LenghtSeriesError(SeriesValidation):
    """Se lanza cuando la serie no tiene la longitud correcta."""

    pass


class PeriodSeriesError(SeriesValidation):
    """Se lanza cuando la serie no tiene el periodo correcta."""

    pass


class DocumentTypeSeriesError(SeriesValidation):
    """Se lanza cuando la serie no tiene el periodo correcta. debe estar en 20250100"""

    pass


class DateTimeSeriesError(SeriesValidation):
    """Se lanza cuando la serie no tiene el periodo correcta. debe estar en 04/01/2022"""

    pass


class DateTimeTransformError(SeriesValidation):
    """Se lanza cuando la serie no no se pudo transformar a datetime"""

    pass


class NumberVoucherSeriesError(SeriesValidation):
    """Se lanza cuando la serie no son datos Numericos ejemplo:'121'. numero de comprbante inicial y final"""

    pass


class ValueSeriesError(SeriesValidation):
    """Se lanza cuando la serie no teine los datos esperados"""

    pass


class NumericSeriesError(SeriesValidation):
    """Se lanza cuando la serie no es numerica"""

    pass


class TransformSeriesToNumericError(SeriesValidation):
    """Se lanza cuando la serie no se pudo transformar a numerico"""

    pass

from dataclasses import dataclass
from pandas import Series, DataFrame, to_datetime, to_numeric
from datetime import date
from rpa_paredes_cano_ventas.exceptions.series import (
    SeriesEmptyError,
    LenghtSeriesError,
    PeriodSeriesError,
    DocumentTypeSeriesError,
    DateTimeSeriesError,
    DateTimeTransformError,
    # NumberVoucherSeriesError,  # f"Series[{name}] some values are not numeric."
    ValueSeriesError,
    NumericSeriesError,
    TransformSeriesToNumericError,
)


@dataclass(frozen=True, slots=True)
class SeriesValidator:
    # 1. Evita que se cree un diccionario de atributos (__dict__) para la clase.
    # Al estar vacío, la clase no puede tener variables de instancia.
    # --- Validaciones de Existencia y Formato Básico ---
    @classmethod
    def check_exists_and_not_empty(cls, series: Series, name: str) -> None:
        # Optimizamos usando .values para evaluar rapidez fuera del índice de pandas
        is_empty = series.isna() | (series.astype(str).str.strip() == "")
        if is_empty.any():
            raise SeriesEmptyError(f"Series[{name}] some values are empty.")

    @classmethod
    def check_length(cls, series: Series, name: str, length: int) -> None:
        if (series.astype(str).str.strip().str.len() != length).any():
            raise LenghtSeriesError(
                f"Series[{name}] some values are not the correct {str(length)} length."
            )

    @classmethod
    def to_numeric(cls, series: Series, name: str):
        """Ahorro de memoria: No creamos una copia de la serie si no es necesario."""
        try:
            series = to_numeric(series)
        except:
            raise TransformSeriesToNumericError(
                f"[{name}] cannot be transformed to numeric."
            )
        return series.round(2)

    # --- Validaciones de Negocio ---

    @classmethod
    def validate_period(cls, series: Series, name: str, period_date: date):
        format_period = period_date.strftime("%Y%m") + "00"  # 20250100
        cls.check_exists_and_not_empty(series, name)
        correct_date = (series.str.strip() == format_period).all()
        if not correct_date:
            raise PeriodSeriesError(
                f"Series[{name}] some values are not the correct period:{period_date}."
            )

    @classmethod
    def validate_datetime(cls, series: Series, name: str, period_date: date):
        current_month = period_date.day
        current_year = period_date.year
        is_correct_date = (
            (series.dt.month == current_month) & (series.dt.year == current_year)
        ).all()
        if not is_correct_date:
            raise DateTimeSeriesError(
                f"Series[{name}] some values are not the correct period:{period_date}."
            )

    @classmethod
    def to_datetime(cls, series: Series, name: str) -> Series:
        try:
            series = to_datetime(series)
        except ValueError:
            raise DateTimeTransformError(
                f"Series[{name}] some values are not datetime."
            )
        return series

    @classmethod
    def validate_document_type(
        cls, series: Series, name: str, allowed=("01", "03", "07", "08")
    ):
        """Usamos una tupla en 'allowed' porque las tuplas son más ligeras que las listas."""
        cls.lenght_specific_series(series, name, [2])
        if (~series.isin(allowed)).any():
            raise DocumentTypeSeriesError(
                f"Series[{name}] some values are not the correct. Allowed: {str(allowed)}"
            )

    @classmethod
    def validate_conditional_negative(cls, series: Series, col_f: Series, name: str):
        # Acceso directo por máscara para no duplicar datos en memoria
        if (series[(col_f == "07")] >= 0).any():
            raise ValueError(
                f"[{name}] Debe ser negativo cuando el Tipo Doc (F) es 07."
            )

    @classmethod
    def validate_reference_info(cls, df: DataFrame, col_f_name: str, ref_cols: list):
        mask_f_special = df[col_f_name].isin(["07", "08"])
        for col in ref_cols:
            # Validación directa sobre el DataFrame original para ahorrar RAM
            check = df.loc[mask_f_special, col]
            if check.isna().any() or (check.astype(str).str.strip() == "").any():
                raise ValueError(
                    f"[{col}] Es obligatorio cuando Tipo Doc (F) es 07 o 08."
                )

    @classmethod
    def clean_razon_social(cls, series: Series) -> Series:
        """Modifica la serie y la devuelve (Pandas maneja la optimización interna)."""
        # r"[^a-zA-Z0-9\s]"
        patron = r"['`´,‘’“\"‘]"
        return series.astype(str).str.replace(patron, "", regex=True)

    @classmethod
    def validate_business_segment(
        cls, series: Series, allowed=("Isadora", "Toda Moda")
    ):
        cls.check_exists_and_not_empty(series, "Segmento (AJ)")
        # Usamos tupla para categorías fijas
        if (~series.isin(allowed)).any():
            raise ValueError(f"Segmento (AJ) debe ser 'Isadora' o 'Toda Moda'.")

    @classmethod
    def validate_datetime_emision(
        cls, series: Series, name: str, period_date: date
    ) -> Series:
        cls.check_exists_and_not_empty(series, name)
        series = cls.to_datetime(series, name)
        cls.validate_datetime(series, name, period_date)
        return series.dt.strftime("%d/%m/%Y")

    @classmethod
    def to_dateime_raise(cls, series: Series, name: str) -> Series:
        series_dt = to_datetime(series, errors="coerce", dayfirst=True)

        # 2. Si hay NaNs que originalmente NO estaban vacíos, levantamos el error
        # Comparamos contra la serie original descartando los nulos reales
        if series_dt.isna().any():
            # Identificamos los valores que causaron el fallo
            invalid_mask = (
                series_dt.isna()
                & series.notna()
                & (series.astype(str).str.strip() != "")
            )
            invalid_values = series[invalid_mask].unique()

            if len(invalid_values) > 0:
                raise ValueError(
                    f"❌ Error crítico de formato en fechas:\n"
                    f"Los siguientes valores no son fechas válidas: {list(invalid_values)}\n"
                    f"Se esperaba el formato Día/Mes/Año."
                )

        return series_dt

    @classmethod
    def validate_datetime_vencimiento(
        cls, series: Series, name: str, period_date: date
    ) -> Series:
        # puede tener fechas vacias
        # como esta series puede tener fechas vacias, no podemos usar check_exists_and_not_empty
        # pero debo quitar los valores vacios o none para pasar a datetime
        series = series[series.notna() & (series.str.strip() != "")]
        series = cls.to_datetime(series, name)
        cls.validate_datetime(series, name, period_date)
        return series.dt.strftime("%d/%m/%Y")

    @classmethod
    def validate_document_number(cls, series: Series, name: str):
        pass

    @classmethod
    def validate_type_comprobante(cls, series: Series, name: str, allowed: tuple[str]):
        """valida el tipo comprobante"""
        # 01 03
        cls.check_exists_and_not_empty(series, name)
        cls.lenght_specific_series(series, name, [2])
        cls.validate_fixture(series, name, allowed)

    @classmethod
    def validate_number_series_comprobante(cls, series: Series, name: str):
        """valida el numero serie comprobante"""
        # F006
        cls.check_exists_and_not_empty(series, name)
        cls.lenght_specific_series(series, name, [4])

    @classmethod
    def validate_numeric(cls, series: Series, name: str):
        is_all_numeric = series.str.isnumeric().all()
        if not is_all_numeric:
            raise NumericSeriesError(f"Series[{name}] some values are not numeric.")

    @classmethod
    def validate_number_comprobante(cls, series: Series, name: str):
        """valida el numero comprobante inicial y final"""
        cls.check_exists_and_not_empty(series, name)
        cls.validate_numeric(series, name)

    @classmethod
    def validate_fixture(cls, series: Series, name: str, allowed=tuple):
        if (~series.isin(allowed)).any():
            raise ValueSeriesError(
                f"Series[{name}] some values are not the correct. Allowed: {str(allowed)}"
            )

    @classmethod
    def validate_type_document_client(
        cls, series: Series, name: str, allowed: tuple[str]
    ):
        # las series puede tener valores vacios
        # filtras esos valores
        series: Series = series[series.notna() & (series.str.strip() != "")]
        cls.lenght_specific_series(series, name, [2])
        cls.validate_fixture(series, name, allowed)

    @classmethod
    def lenght_specific_series(cls, series: Series, name: str, length: list):
        # 1. Limpiamos y obtenemos las longitudes
        lengths = series.astype(str).str.strip().str.len()
        # 2. Verificamos que NO cumpla ni con 8 ni con 10
        # El operador ~ es "NOT", invertimos la máscara para hallar los errores
        errores = ~lengths.isin(length)
        if errores.any():
            raise LenghtSeriesError(
                f"Series[{name}] some values are not the correct. length: {str(length)}"
            )

    @classmethod
    def validate_number_id(cls, series: Series, name: str):
        cls.check_exists_and_not_empty(series, name)
        cls.validate_numeric(series, name)
        # la longitud debe ser 8 o 10 digitos...
        cls.lenght_specific_series(series, name, [8, 10])

    @classmethod
    def clean_bi_igv_import(cls, series: Series, name: str) -> Series:
        cls.check_exists_and_not_empty(series, name)
        series = series.astype(str).str.replace(",", ".", regex=False)
        series = cls.to_numeric(series, name)
        return series

    @classmethod
    def validate_segmento_negocio(cls, series: Series, name: str, allowed=tuple):
        cls.check_exists_and_not_empty(series, name)
        cls.validate_fixture(
            series=series,
            name=name,
            allowed=allowed,
        )

    @classmethod
    def validate_sucursal(cls, series: Series, name: str):
        cls.check_exists_and_not_empty(series, name)

    @classmethod
    def format_date(cls, series: Series, name: str) -> Series:
        series = cls.to_datetime(series, name)
        return series.dt.strftime("%d/%m/%Y")

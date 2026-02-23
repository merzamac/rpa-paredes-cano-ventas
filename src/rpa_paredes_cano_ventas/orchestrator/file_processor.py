from dataclasses import dataclass
from pathlib import Path
from rpa_paredes_cano_ventas.models.processable import (
    ProcessableFile,
    ProcessedFolder,
)
from rpa_paredes_cano_ventas.readers.read_input_output import (
    ReadInputDir,
    ReadOutputDir,
)
from rpa_paredes_cano_ventas.interfaces.base import FileDataReader
from rpa_paredes_cano_ventas.models.header import Header
from rpa_paredes_cano_ventas.models.validators import SeriesValidator
from rpa_paredes_cano_ventas.processor.export import Export
from pathlib import Path
from loguru import logger
from pandas import DataFrame, Series
from datetime import date
from rpa_paredes_cano_ventas.models.processable import (
    ProcessableFile,
)
from rpa_paredes_cano_ventas.types import DAtaCSV


class FileProcessor:
    def __init__(self) -> None:
        pass

    def get_pending_files(
        self, input_dir: Path, output_dir: Path
    ) -> tuple[ProcessableFile, ...]:
        """Obtiene los archivos pendientes de procesamiento."""

        processable_input_files: tuple[ProcessableFile, ...] = ReadInputDir.execute(
            input_dir=input_dir
        )
        processable_output_folders: tuple[ProcessedFolder, ...] = ReadOutputDir.execute(
            output_dir=output_dir
        )

        input_files_to_process: set[ProcessableFile] = set(
            processable_input_files
        ) - set(processable_output_folders)

        return tuple(input_files_to_process)

    def create_massive_csv(
        self,
        reader: FileDataReader,
        processable: ProcessableFile,
        output_dir: Path,
        batch_size: int,
    ) -> None:
        logger.info(f"Iniciando procesamiento de: {processable.file_path}")
        int_sheet_name = 0
        start = 1
        output_dir = output_dir / processable.output_path
        files: list[Path] = []
        export = Export(output_path=output_dir)
        for i, chunk in enumerate(reader.get_data(processable.file_path, batch_size)):

            int_sheet_name += len(chunk)
            # reglas de negocio para el bloque de datos
            chunk = self._clean_and_validate(
                chunk, int_sheet_name, processable.period_date
            )
            chunk = self._make_maviso(chunk, start, int_sheet_name)
            files.append(export.csv(chunk, output_dir, int_sheet_name))
            export.add_block(chunk)
            start = int_sheet_name + 1
        export.close()
        logger.info("Procesamiento finalizado con éxito.")
        # MakeXLSXIxport.execute(files, output_dir)
        return DAtaCSV(period=processable.period_date, files=tuple(files))

    def _make_maviso(
        self,
        chunk: DataFrame,
        start: int,
        int_sheet_name: int,
    ) -> DataFrame:
        index = Series(range(start, int_sheet_name + 1), index=range(len(chunk)))
        chunk = DataFrame(
            {
                "No": index,
                "Periodo": chunk[Header.periodo],
                "FechaComprobante": chunk[Header.fecha_emision],
                "FechaVencimiento": chunk[Header.fecha_vencimiento],
                "CodigoTipoComprobante": chunk[Header.tipo_comprobante],
                "NumeroSerieComprobante": chunk[Header.serie_comprobante],
                "NumeroComprobanteInicial": chunk[Header.nro_comprobante_ini],
                "NumeroComprobanteFinal": chunk[Header.nro_comprobante_fin],
                "CodigoTipoDocumentoIdentidad": chunk[Header.tipo_doc_cliente],
                "NumeroDocumentoIdentidad": chunk[Header.nro_doc_cliente],
                "NombreCliente": chunk[Header.nombre_razon_social],
                "ImporteAfecto": chunk[Header.bi_gravado],
                "ImporteImpuesto": chunk[Header.igv_gravado],
                "ImporteTotal": chunk[Header.importe],
                "FechaComprobanteModificado": chunk[Header.fecha_modifica],
                "CodigoTipoComprobanteModificado": chunk[Header.tipo_modifica],
                "NumeroSerieComprobanteModificado": chunk[Header.serie_modifica],
                "NumeroComprobanteModificado": chunk[Header.nro_modifica],
                "Negocio": chunk[Header.segmento_negocio],
                "Sucursal": chunk[Header.sucursal],
            }
        )
        return chunk

    def _clean_and_validate(
        self, chunk: DataFrame, int_sheet_name: int, period_date: date
    ):
        logger.info(f"Procesando bloque {int_sheet_name} con {len(chunk)} registros...")

        SeriesValidator.validate_period(
            series=chunk[Header.periodo],
            name=Header.periodo,
            period_date=period_date,
        )
        chunk[Header.fecha_emision] = SeriesValidator.validate_datetime_emision(
            series=chunk[Header.fecha_emision],
            name=Header.fecha_emision,
            period_date=period_date,
        )
        chunk[Header.fecha_vencimiento] = SeriesValidator.validate_datetime_vencimiento(
            series=chunk[Header.fecha_vencimiento],
            name=Header.fecha_vencimiento,
            period_date=period_date,
        )
        SeriesValidator.validate_type_comprobante(
            series=chunk[Header.tipo_comprobante],
            name=Header.tipo_comprobante,
            allowed=("01", "03", "07", "08"),
        )

        SeriesValidator.validate_number_series_comprobante(
            series=chunk[Header.serie_comprobante], name=Header.serie_comprobante
        )

        SeriesValidator.validate_number_comprobante(
            series=chunk[Header.nro_comprobante_ini], name=Header.nro_comprobante_fin
        )
        SeriesValidator.validate_number_comprobante(
            series=chunk[Header.nro_comprobante_fin], name=Header.nro_comprobante_fin
        )
        SeriesValidator.validate_type_document_client(
            series=chunk[Header.tipo_doc_cliente],
            name=Header.tipo_doc_cliente,
            allowed=("01", "06"),
        )
        chunk[Header.nombre_razon_social] = SeriesValidator.clean_razon_social(
            series=chunk[Header.nombre_razon_social],
        )
        chunk[Header.bi_gravado] = SeriesValidator.clean_bi_igv_import(
            series=chunk[Header.bi_gravado],
            name=Header.bi_gravado,
        )
        chunk[Header.igv_gravado] = SeriesValidator.clean_bi_igv_import(
            series=chunk[Header.igv_gravado],
            name=Header.igv_gravado,
        )
        chunk[Header.importe] = SeriesValidator.clean_bi_igv_import(
            series=chunk[Header.importe],
            name=Header.importe,
        )
        SeriesValidator.validate_segmento_negocio(
            series=chunk[Header.segmento_negocio],
            name=Header.segmento_negocio,
            allowed=("Isadora", "Todo Moda"),
        )
        SeriesValidator.validate_sucursal(
            series=chunk[Header.sucursal],
            name=Header.sucursal,
        )
        #########################validacion especifica de negocio####################################
        df_special = chunk[chunk[Header.tipo_comprobante].isin(["07", "08"])].copy()
        # las siguientes reglas son para las columnas donde el tipo de comprobantes es 07 u 08
        # en las 4 columnas deben existir datos y en dos de ellas el data debe tener longitud 2
        SeriesValidator.check_exists_and_not_empty(
            df_special[Header.fecha_modifica], Header.fecha_modifica
        )
        SeriesValidator.check_exists_and_not_empty(
            df_special[Header.tipo_modifica], Header.tipo_modifica
        )

        SeriesValidator.check_exists_and_not_empty(
            df_special[Header.serie_modifica], Header.serie_modifica
        )
        SeriesValidator.check_exists_and_not_empty(
            df_special[Header.nro_modifica], Header.fecha_emision
        )
        SeriesValidator.lenght_specific_series(
            df_special[Header.tipo_modifica], Header.tipo_modifica, [2]
        )

        SeriesValidator.lenght_specific_series(
            df_special[Header.serie_modifica], Header.serie_modifica, [4]
        )
        chunk[Header.fecha_modifica] = SeriesValidator.format_date(
            series=chunk[Header.fecha_modifica],
            name=Header.fecha_modifica,
        )
        return chunk

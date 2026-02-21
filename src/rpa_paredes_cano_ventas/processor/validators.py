from rpa_paredes_cano_ventas.exceptions.structure_sunat import (
    DifferentTemplateLengthError,
)


class PLEValidator:
    """Clase especializada en validar la integridad de archivos PLE."""

    @staticmethod
    def header_structure(first_row_ws, header_desc_cls) -> None:
        # 1. Preparar headers (Excel vs Template)
        header = tuple(str(cell.value).strip().lower() for cell in first_row_ws)
        fields_template = fields(header_desc_cls)
        header_template = tuple(f.default for f in fields_template)

        # 2. Validar Longitud
        if len(header) != len(header_template):
            raise DifferentTemplateLengthError(len(header), len(header_template))

        # 3. Validar Contenido y Orden
        for index_column, column_template in enumerate(header_template):
            column_data = header[index_column]
            if column_data != column_template:
                # Obtenemos el nombre del atributo (ej: 'periodo') para el error
                attr_name = fields_template[index_column].name
                raise ColumnMismatchTemplateError(
                    index_column, column_data, column_template, attr_name
                )

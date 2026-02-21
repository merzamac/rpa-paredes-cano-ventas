from rpa_paredes_cano_ventas.types import UtilityMut


class Header(metaclass=UtilityMut):
    __slots__ = []
    """
    HEADER DE LA HOJA DE SUNAT
    """

    periodo: str = "Periodo"
    tipo_cuo: str = "Tipo CUO"
    nro_cuo: str = "Nº CUO"
    fecha_emision: str = "Fecha Emisión comprobante"
    fecha_vencimiento: str = "Fecha de vencimiento"
    tipo_comprobante: str = "Tipo\nComprobante"
    serie_comprobante: str = "Serie Comprobante "
    nro_comprobante_ini: str = "Nº Comprobante Inicial"
    nro_comprobante_fin: str = "Nº Comprobante Final"
    dif: str = "DIF"
    tipo_doc_cliente: str = "Tipo de Doc. Cliente"
    nro_doc_cliente: str = "Nº de Doc. Cliente"
    nombre_razon_social: str = "Nombre/Razon Social"
    bi_exportacion: str = "BI._Exportacion"
    bi_gravado: str = "BI Adq. Vtas. Grav"
    dscto_bi: str = "DSCTO BI"
    igv_gravado: str = "IGV Adq. Vtas. Grav"
    dscto_igv: str = "DSCTO IGV"
    exonerado: str = "Imp. Total Adquicisiones exoneradas"
    inafecto: str = "Imp. Total Operaciones Inafectas"
    isc: str = "ISC"
    bi_arroz: str = "BI. Operaciones Gravadas C/ el IGV del Arroz Pilado"
    igv_arroz: str = "Imp. A las Ventas del Arroz Pilado"
    otros: str = "Otros"
    importe: str = "Importe"
    moneda: str = "COD MONEDA"
    tipo_cambio: str = "Tipo Cambio"
    fecha_modifica: str = "Fecha Emision Comprobantes Pago que Modifica"
    tipo_modifica: str = "Tipo Comprobante Pago Modifica"
    serie_modifica: str = "Nº Serie Comprobante Modifica"
    nro_modifica: str = "Nº Comprobante Pago Modifica"
    id_contrato: str = "IDENTIF DEL CONTRATO"
    error_1: str = "ERROR TIPO 1"
    indicador_cp: str = "INDICADOR COMPROBANTES DE PAGO"
    estado: str = "Estado"
    segmento_negocio: str = "SegmentoDeNegocio"
    sucursal: str = "Sucursal"
    nro_caja: str = "Nro_Caja"
    centro_costo: str = "CENTRO DE COSTO"


class MetaInmutable(type):
    """
    Metaclase para proteger HeaderPLE contra modificaciones.
    """

    def __setattr__(cls, name, value):
        raise AttributeError("HeaderPLE es inmutable. No puedes cambiar los índices.")


class HeaderPLE(metaclass=MetaInmutable):
    """
    Mapeo de índices autogenerado desde HeaderDescripcion.
    Uso: row[HeaderPLE.moneda] -> Accede a la columna 25.
    """

    __slots__ = ()
    # Generación dinámica de índices (periodo=0, tipo_cuo=1, etc.)
    # for i, campo in enumerate(fields(HeaderDescripcion)):
    #     locals()[campo.name] = i

    def __init__(self):
        raise TypeError("HeaderPLE es estática y no puede ser instanciada.")

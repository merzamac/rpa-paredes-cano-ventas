from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional
import re


class RegistroMaestro(BaseModel):
    model_config = ConfigDict(
        # frozen=True,  # Hace al objeto inmutable y hashable
        arbitrary_types_allowed=True,  # Permite tipos fuera de los estándar si fuera necesario
        str_strip_whitespace=True,  # Limpia espacios automáticamente
        str_to_upper=True,  # Pydantic V2 puede forzar mayúsculas automáticamente
    )

    # Campos base
    """
    Almacena registros maestros de ACONSYS con validación de datos.
    """
    # Campos obligatorios
    serie: str = Field(..., min_length=4, description="Serie del documento")
    sucursal: str = Field(..., min_length=1, description="Código de sucursal")

    # Centro de Costo (opcional)
    centro_costo: Optional[str] = None
    descripcion_cc: Optional[str] = None

    # Tipo de Operación (opcional)
    tipo_oper: Optional[str] = None
    descripcion_oper: Optional[str] = None

    # Cuenta Corriente (opcional)
    cuenta_corriente: Optional[str] = None
    descripcion_cta: Optional[str] = None

    tipo_serie: Optional[str] = None  # Se calculará automáticamente

    @model_validator(mode="after")
    def determinar_tipo_serie(self) -> "RegistroMaestro":
        """
        Analiza el prefijo de la serie para clasificarla.
        """
        s = self.serie.upper()

        if s.startswith("BMO"):
            self.tipo_serie = "BMOX"
        elif s.startswith("FMO"):
            self.tipo_serie = "FMOX"
        elif s.startswith("EB"):
            self.tipo_serie = "EBXX"
        elif s.startswith("B"):
            self.tipo_serie = "BXXX"
        elif s.startswith("F"):
            self.tipo_serie = "FXXX"
        elif s.startswith("E"):
            self.tipo_serie = "EXXX"
        elif s.isdigit():
            self.tipo_serie = "XXXX"
        else:
            raise ValueError("Se desconoce el tipo de serie.")

        return self

    @field_validator("serie", "sucursal", mode="before")
    @classmethod
    def trim_strings(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    def __eq__(self, other: object) -> bool:
        # Define que dos objetos son "iguales" si serie y sucursal coinciden
        if not isinstance(other, RegistroMaestro):
            return False
        return self.serie == other.serie and self.sucursal == other.sucursal

    def __hash__(self) -> int:
        return hash((self.serie, self.sucursal))

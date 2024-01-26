from typing import List

import pydantic


class CampoMetadata(pydantic.BaseModel):
    """Datos posicionales de un campo en un fichero con campos de longitud fija."""

    field_name_in_class: str
    """Nombre del campo en el modelo/clase."""

    clave: str
    """Clave de campo usada por DGT."""
    posicion: int
    """Posición del campo en fichero original."""
    longitud: int
    """Longitud del campo en fichero original."""

    @classmethod
    def from_docstring(cls, field_name: str, docstring_lines: List[str]) -> "CampoMetadata":
        kwargs = dict()
        for line in docstring_lines:
            chunks = line.split("=")
            if len(chunks) == 2:
                key, value = chunks
                kwargs[key] = value

        return cls(field_name_in_class=field_name, **kwargs)


class ParseError(pydantic.BaseModel):
    exception: Exception
    line_number: int
    line_content: str
    parsed_fields: dict

    class Config(pydantic.BaseModel.Config):
        arbitrary_types_allowed = True

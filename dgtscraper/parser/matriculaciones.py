from typing import Generator, Union, TextIO

from ..models.matriculaciones import Matriculacion
from ..models.common import ParseError


def parse_matriculaciones_file(file: TextIO) -> Generator[Union[Matriculacion, ParseError], None, None]:
    i = 0
    for line in file:
        i += 1
        if not line or line.startswith("Vehículos matriculados"):
            continue

        kwargs = _parse_matriculaciones_line_to_kwargs(line)
        try:
            if not kwargs["bastidor"].strip():
                # Ignorar matriculaciones sin bastidor
                # TODO Parametrizar posibilidad de obtener estas matriculaciones con un valor generico para el bastidor
                continue

            yield Matriculacion(**kwargs)

        except Exception as ex:
            yield ParseError(
                exception=ex,
                line_number=i,
                line_content=line,
                parsed_fields=kwargs,
            )


def _parse_matriculaciones_line_to_kwargs(line: str) -> dict:
    kwargs = dict()
    index_start = 0
    for field_metadata in Matriculacion.get_fields_metadata():
        index_end = index_start + field_metadata.longitud
        value = line[index_start:index_end]
        index_start = index_end
        kwargs[field_metadata.field_name_in_class] = value.strip()

    return kwargs

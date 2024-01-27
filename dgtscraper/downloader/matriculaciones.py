import pathlib
import tempfile
from typing import Optional, Union, Generator

import bs4
import requests
from stream_unzip import stream_unzip


class DGTDownloader:
    def __init__(self):
        self.unzip_chunk_size = 65536
        self.tmp_path = pathlib.Path(tempfile.gettempdir()) / "dgtparser"

        self.tmp_path.mkdir(exist_ok=True)
        self.session = requests.Session()

        self._last_viewstate = ""
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
        })

    def download_matriculaciones_by_date(
            self,
            year: int,
            month: int,
            day: Optional[int] = None,
            path: Union[pathlib.Path, str, None] = None
    ) -> pathlib.Path:
        # TODO Fix download matriculaciones per day
        if path and isinstance(path, str):
            path = pathlib.Path(path)

        if not path or path.is_dir():
            if day:
                filename = f"matriculaciones-{year}-{month:02d}-{day:02d}.txt"
            else:
                filename = f"matriculaciones-{year}-{month:02d}.txt"

            if not path:
                path = pathlib.Path().absolute() / filename
            else:
                path = path / filename

        path.touch(exist_ok=True)

        with open(path, "w") as output_file:
            for chunk in self.stream_matriculaciones_by_date(year=year, month=month, day=day):
                output_file.write(chunk)

        return path

    def stream_matriculaciones_by_date(
            self,
            year: int,
            month: int,
            day: Optional[int] = None,
    ) -> Generator[str, None, None]:
        self._get_viewstate_0()
        self._get_viewstate_1_vehiculos()
        self._get_viewstate_2_vehiculos_matriculaciones()
        self._get_viewstate_3_microdatos()

        filtro_diario = ""
        if day:
            filtro_diario = f"{day:02d}/{month:02d}/{year}"

        payload = {
            "configuracionInfPersonalizado": "configuracionInfPersonalizado",
            "configuracionInfPersonalizado:filtroDiario": filtro_diario,
            "configuracionInfPersonalizado:filtroMesAnyo": str(year),
            "javax.faces.ViewState": self._last_viewstate,
        }
        if day:
            payload["configuracionInfPersonalizado:j_id115"] = "Descargar"
            payload["configuracionInfPersonalizado:filtroMesMes"] = "1"
        else:
            payload["configuracionInfPersonalizado:j_id131"] = "Descargar"
            payload["configuracionInfPersonalizado:filtroMesMes"] = str(month)

        response = self.session.post(
            "https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/microdatos.faces",
            data=payload,
            stream=True,
        )
        response.raise_for_status()

        # TODO Parsear posibles errores (en el HTML se imprime el error)

        for chunk in self._unzip_stream_response(response):
            yield chunk.decode("iso-8859-1")

    def _get_viewstate_0(self):
        response = self.session.get("https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/categoria.faces")
        self._parse_viewstate(response)

    def _get_viewstate_1_vehiculos(self):
        payload = {
            "menu": "menu",
            "menu:listadoMenu:0:j_id49": "Veh%EDculos",
            "javax.faces.ViewState": self._last_viewstate,
        }
        response = self.session.post(
            url="https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/categoria.faces",
            data=payload,
        )
        self._parse_viewstate(response)

    def _get_viewstate_2_vehiculos_matriculaciones(self):
        payload = {
            "menu": "menu",
            "menu:listadoMenu:0:listadoSubMenu:3:j_id42": "Matriculaciones",
            "javax.faces.ViewState": self._last_viewstate,
        }
        response = self.session.post(
            url="https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/categoria.faces",
            data=payload,
        )
        self._parse_viewstate(response)

    def _get_viewstate_3_microdatos(self):
        payload = {
            "accesoInformes": "accesoInformes",
            "accesoInformes:listadoInformesExternos:2:j_id95": "Microdatos",
            "javax.faces.ViewState": self._last_viewstate,
        }
        response = self.session.post(
            url="https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/subcategoria.faces",
            data=payload,
        )
        self._parse_viewstate(response)

    def _parse_viewstate(self, response: requests.Response) -> str:
        parser = bs4.BeautifulSoup(response.text)
        self._last_viewstate = parser.find("input", {"name": "javax.faces.ViewState"}).get("value")
        return self._last_viewstate

    def _unzip_stream_response(self, response: requests.Response) -> Generator[bytes, None, None]:
        files_read = 0
        for _, _, file_chunks in stream_unzip(response.iter_content(chunk_size=self.unzip_chunk_size)):
            if files_read > 0:
                break

            files_read += 1
            buffer = b""
            for chunk in file_chunks:  # type: bytes
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    line += b"\n"
                    yield line

            if buffer:
                yield buffer

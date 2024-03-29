import pathlib
import tempfile
import datetime
from typing import Optional, Union, Generator

import bs4
import requests
from stream_unzip import stream_unzip

from .. import const


class DGTDownloader:
    def __init__(self):
        self.unzip_chunk_size = const.DEFAULT_DOWNLOAD_CHUNK_SIZE
        self.tmp_path = pathlib.Path(tempfile.gettempdir()) / "dgtparser"
        self.bs4_features = "html.parser"

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
        if not day:
            self._get_viewstate_4_year(year)

        payload = {
            "configuracionInfPersonalizado": "configuracionInfPersonalizado",
            "javax.faces.ViewState": self._last_viewstate,
        }

        # download by day
        if day:
            prev_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
            payload.update({
                "configuracionInfPersonalizado:j_id115": "Descargar",
                "configuracionInfPersonalizado:filtroDiario": f"{day:02d}/{month:02d}/{year}",
                "configuracionInfPersonalizado:filtroMesMes": str(prev_month.month),
                "configuracionInfPersonalizado:filtroMesAnyo": str(prev_month.year),
            })

        # download by month
        else:
            payload.update({
                "configuracionInfPersonalizado:j_id131": "Descargar",
                "configuracionInfPersonalizado:filtroDiario": "",
                "configuracionInfPersonalizado:filtroMesMes": str(month),
                "configuracionInfPersonalizado:filtroMesAnyo": str(year),
            })

        response = self.session.post(
            "https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/microdatos.faces",
            data=payload,
            stream=True,
        )
        self._validate_response(response)

        for chunk in self._unzip_stream_response(response):
            yield chunk.decode(const.FILE_ENCODING)

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

    def _get_viewstate_4_year(self, year: int):
        """Called after choosing a year, for filtering by month.
        """
        payload = {
            "": "",
            "AJAXREQUEST": "_viewRoot",
            "configuracionInfPersonalizado": "configuracionInfPersonalizado",
            "configuracionInfPersonalizado:filtroDiario": "",
            "configuracionInfPersonalizado:filtroMesAnyo": str(year),
            "configuracionInfPersonalizado:filtroMesMes": "1",
            "configuracionInfPersonalizado:j_id127": "configuracionInfPersonalizado:j_id127",
            "javax.faces.ViewState": self._last_viewstate,
        }
        response = self.session.post(
            url="https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/microdatos.faces",
            data=payload,
        )
        self._parse_viewstate(response)

    def _validate_response(self, response: requests.Response):
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "zip" in content_type:
            return
        if "html" not in content_type:
            raise ValueError(f"Unknown response content type ({content_type})")

        error = self._parse_error(response) or "Unknown"
        raise ValueError(f"DGT Error: {error}")

    def _parse_viewstate(self, response: requests.Response) -> str:
        parser = bs4.BeautifulSoup(response.text, features=self.bs4_features)
        self._last_viewstate = parser.find("input", {"name": "javax.faces.ViewState"}).get("value")
        return self._last_viewstate

    def _parse_error(self, response: requests.Response) -> str:
        parser = bs4.BeautifulSoup(response.text, features=self.bs4_features)
        error_li = parser.find("li", {"class": "msgError"})
        if error_li:
            return error_li.text

    def _unzip_stream_response(self, response: requests.Response) -> Generator[bytes, None, None]:
        response_iterator = response.iter_content(chunk_size=self.unzip_chunk_size)
        for _, _, file_chunks_iterator in stream_unzip(response_iterator):
            # Only a single txt file expected in the zip

            buffer = b""
            for chunk in file_chunks_iterator:  # type: bytes
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    line += b"\n"
                    yield line

            if buffer:
                yield buffer

            break

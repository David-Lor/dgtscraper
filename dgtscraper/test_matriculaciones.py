import datetime
import hashlib
import json

import pytest

from dgtscraper.downloader import DGTDownloader
from dgtscraper.parser import parse_matriculaciones_line
from dgtscraper.models import Matriculacion, ParseError


def matriculacion_to_sorted_json(matriculacion: Matriculacion) -> str:
    js = matriculacion.json()
    dc = json.loads(js)
    return json.dumps(dc, sort_keys=True)


@pytest.mark.parametrize("year,month,day,expected_md5,expected_count", [
    pytest.param(2024, 1, None, "739aa8771557bbc25eb44ffe0bed2596", 117036, id="2024/01"),
    pytest.param(2023, 12, None, "a3244af834ade58f73082a2c2a0c46f5", 127658, id="2023/12"),
    pytest.param(2023, 10, None, "5fee9a71f5ff31299083f12fc9859d07", 141045, id="2023/10"),
    pytest.param(2023, 7, None, "160ac3aad4ddb525e98086da0555013a", 138417, id="2023/07"),
    pytest.param(2023, 1, None, "ca0308aa7fd039249162af385481803a", 107492, id="2023/01"),
    pytest.param(2020, 3, None, "090a3f8d7634901555869551ddd70507", 64218, id="2020/03"),
    pytest.param(2016, 6, None, "c890443f8dff95b0bd7758748a0f9943", 178890, id="2016/06"),
    pytest.param(2014, 12, None, "780364808644082e2279ee13b79ab297", 99890, id="2014/12"),
])
def test_matriculaciones_stream_to_md5(year, month, day, expected_md5, expected_count):
    scraper = DGTDownloader()
    md5 = hashlib.md5()
    parsed_count = 0

    # noinspection PyTypeChecker
    for line in scraper.stream_matriculaciones_by_date(year, month, day):
        matriculacion = parse_matriculaciones_line(line)
        if not matriculacion:
            continue

        matriculacion_json = matriculacion_to_sorted_json(matriculacion)
        md5.update(matriculacion_json.encode())
        parsed_count += 1

    assert parsed_count == expected_count
    assert md5.hexdigest() == expected_md5


def test_matriculaciones_per_day():
    """Download matriculaciones from a few days ago.
    Downloading by day returns provisional data, is not always available and gets removed periodically.
    Can only assert that a few matriculaciones are returned, and no parse errors occurred.
    """
    date = datetime.date.today() - datetime.timedelta(days=3)
    scraper = DGTDownloader()
    parsed_count = 0
    error_count = 0

    for line in scraper.stream_matriculaciones_by_date(year=date.year, month=date.month, day=date.day):
        matriculacion = parse_matriculaciones_line(line)
        if isinstance(matriculacion, Matriculacion):
            parsed_count += 1
        elif isinstance(matriculacion, ParseError):
            error_count += 1

    assert parsed_count > 100
    assert error_count == 0

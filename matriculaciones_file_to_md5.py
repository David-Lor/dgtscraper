import argparse
import hashlib
import json

from dgtscraper.parser import parse_matriculaciones_file
from dgtscraper.models import Matriculacion, ParseError
from dgtscraper.const import FILE_ENCODING


def matriculacion_to_sorted_json(matriculacion: Matriculacion) -> str:
    js = matriculacion.json()
    dc = json.loads(js)
    return json.dumps(dc, sort_keys=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_help = True
    args = parser.parse_args()

    md5 = hashlib.md5()
    parsed_count = 0
    with open(args.file, "r", encoding=FILE_ENCODING) as f:
        for result in parse_matriculaciones_file(f):
            if isinstance(result, ParseError):
                print("Parse Error:", result)
            elif result:
                js = matriculacion_to_sorted_json(result)
                md5.update(js.encode())
                parsed_count += 1

    print("MD5:", md5.hexdigest())
    print("Total parsed matriculaciones:", parsed_count)


if __name__ == '__main__':
    main()

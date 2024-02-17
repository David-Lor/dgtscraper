import argparse

from dgtscraper.parser import parse_matriculaciones_file
from dgtscraper.const import FILE_ENCODING


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_help = True
    args = parser.parse_args()

    with open(args.file, "r", encoding=FILE_ENCODING) as f:
        print("Pulsa Enter tras cada matriculación para ver la siguiente:")
        for result in parse_matriculaciones_file(f):
            if result:
                try:
                    input(result)
                except (KeyboardInterrupt, InterruptedError):
                    break


if __name__ == '__main__':
    main()

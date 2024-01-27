import argparse

from dgtscraper.downloader import DGTDownloader
from dgtscraper.parser import parse_matriculaciones_line


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_help = True
    args = parser.parse_args()

    date = args.date

    date_chunks = date.split("-")
    try:
        year = int(date_chunks[0])
        month = int(date_chunks[1])
    except (KeyError, ValueError):
        print("Invalid date")
        exit(1)

    print("Pulsa Enter tras cada matriculación para ver la siguiente:")
    for matriculacion_str in DGTDownloader().stream_matriculaciones_by_date(year=year, month=month):
        if matriculacion := parse_matriculaciones_line(matriculacion_str):
            try:
                input(matriculacion)
            except (KeyboardInterrupt, InterruptedError):
                break


if __name__ == '__main__':
    main()

import argparse

from dgtscraper.downloader import DGTDownloader
from dgtscraper.parser import parse_matriculaciones_line

# TODO Mover logica de buffer para cada linea a dgtscraper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_help = True
    args = parser.parse_args()

    date = args.date

    date_chunks = date.split("-")
    if len(date_chunks) < 2:
        print("Invalid date")
        exit(1)

    print("Pulsa Enter tras cada matriculación para ver la siguiente:")
    buffer = ""
    for chunk_streamed in DGTDownloader().stream_matriculaciones_by_date(year=int(date_chunks[0]), month=int(date_chunks[1])):
        if "\n" in chunk_streamed:
            chunks = chunk_streamed.split("\n")
            matriculacion_str = buffer + chunks.pop(0)
            if chunks:
                buffer = chunks.pop()
        else:
            buffer += chunk_streamed
            continue

        matriculacion = parse_matriculaciones_line(matriculacion_str)
        if matriculacion:
            try:
                input(matriculacion)
            except (KeyboardInterrupt, InterruptedError):
                break


if __name__ == '__main__':
    main()

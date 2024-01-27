import argparse

from dgtscraper.downloader import DGTDownloader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_argument("-o", "--output", required=False)
    parser.add_help = True
    args = parser.parse_args()

    date = args.date
    output_file = args.output

    date_chunks = date.split("-")
    if len(date_chunks) < 2:
        print("Invalid date")
        exit(1)

    DGTDownloader().download_matriculaciones_by_date(
        year=int(date_chunks[0]),
        month=int(date_chunks[1]),
        path=output_file,
    )


if __name__ == '__main__':
    main()

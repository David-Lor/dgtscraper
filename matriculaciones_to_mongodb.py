import json
import argparse

import pymongo

from dgtscraper.downloader import DGTDownloader
from dgtscraper.parser import parse_matriculaciones_line
from dgtscraper.models import ParseError, Matriculacion


def format_matriculacion_doc(matriculacion: Matriculacion) -> dict:
    doc = json.loads(matriculacion.json())
    doc_id = f"{matriculacion.bastidor}|{matriculacion.fechaTramite.isoformat()}"
    doc["_id"] = doc_id
    return doc


def insert_matriculaciones(mongo_collection: pymongo.collection.Collection, matriculaciones: list[Matriculacion]):
    docs = [format_matriculacion_doc(matri) for matri in matriculaciones]
    result = mongo_collection.bulk_write([pymongo.UpdateOne(
        filter={"_id": doc["_id"]},
        update={"$set": doc},
        upsert=True,
    ) for doc in docs])
    print(f"Inserted {result.upserted_count} docs: {result.upserted_ids}")


# noinspection DuplicatedCode
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("date")
    parser.add_argument("--mongo-uri", required=True)
    parser.add_argument("--mongo-db", required=True)
    parser.add_argument("--mongo-collection", required=True)
    parser.add_argument("--batch-size", type=int, default=10,
                        help="How many matriculaciones to insert per batch")
    parser.add_help = True
    args = parser.parse_args()

    date_chunks = args.date.split("-")
    try:
        year = int(date_chunks[0])
        month = int(date_chunks[1])
        day = int(date_chunks[2]) if len(date_chunks) == 3 else None
    except (KeyError, ValueError):
        print("Invalid date")
        exit(1)

    mongo_collection = pymongo.MongoClient(args.mongo_uri)[args.mongo_db][args.mongo_collection]

    matriculaciones_buffer = list()
    for matriculacion_str in DGTDownloader().stream_matriculaciones_by_date(year=year, month=month, day=day):
        matriculacion = parse_matriculaciones_line(matriculacion_str)
        if not matriculacion:
            continue
        if isinstance(matriculacion, ParseError):
            print(matriculacion)
            continue

        matriculaciones_buffer.append(matriculacion)
        if len(matriculaciones_buffer) >= args.batch_size:
            insert_matriculaciones(mongo_collection, matriculaciones_buffer)
            matriculaciones_buffer.clear()

    if matriculaciones_buffer:
        insert_matriculaciones(mongo_collection, matriculaciones_buffer)


if __name__ == '__main__':
    main()

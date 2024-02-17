# Python DGT Scraper

**Utilidad para descargar y parsear [datasets de matriculaciones de la Dirección General de Tráfico](https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/subcategoria.faces)**

## Requisitos

- Python 3.10 (versiones anteriores podrían funcionar pero no se asegura compatibilidad)
- Probado bajo GNU/Linux (en otros sistemas, los comandos de ejemplo podrían variar)
- Dependencias en [requirements.txt](requirements.txt)

## Matriculaciones

### Descargar

#### CLI

El script [matriculaciones_download](matriculaciones_download.py) descarga y extrae el dataset de matriculaciones, tal y como se presenta en el [portal de microdatos](https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/subcategoria.faces).
Es necesario indicarle un mes o día del que descargar datos.

```bash
python matriculaciones_download.py "año-mes"
python matriculaciones_download.py "año-mes-dia" --output="archivo-salida (opcional)"

# Ejemplos:
python matriculaciones_download.py "2023-01"
python matriculaciones_download.py "2023-04-14"
python matriculaciones_download.py "2023-10" --output="/home/yo/Descargas/2023-Octubre.txt"

# Si no se indica archivo de salida, se descargará en: "./matriculaciones-{año}-{mes}.txt".
# Si se indica un directorio, se creará el archivo en ese directorio.
```

El archivo de salida es un fichero de texto, con codificación iso-8859-1, donde cada línea (excepto la primera) corresponde a una matriculación.
Las columnas tienen [formato de ancho fijo](https://www.ibm.com/docs/es/baw/19.x?topic=formats-fixed-width-format) ([documentación](https://sedeapl.dgt.gob.es/IEST_INTER/pdfs/disenoRegistro/vehiculos/matriculaciones/MATRICULACIONES_MATRABA.pdf)).

### Parsear

El módulo [parser](dgtscraper/parser) carga un archivo de matriculaciones, y parsea cada una de las matriculaciones, utilizando objetos [pydantic](https://github.com/pydantic).

#### CLI

El script [matriculaciones_parse_print](matriculaciones_parse_print.py) lee un archivo de matriculaciones, e imprime cada una de las matriculaciones encontradas,
debidamente parseadas.

```bash
python matriculaciones_parse_print.py "/home/yo/Descargas/2023-Octubre.txt"
```

### Stream

Adicionalmente, se pueden obtener las matriculaciones una a una (línea a línea), sin tener que descargar y descomprimir todo el dataset.

#### CLI

El script [matriculaciones_stream_print](matriculaciones_stream_print.py) lee y descomprime en tiempo real (sin tener que descargar y descomprimir todo el dataset) los datos de matriculaciones.
De esta forma, se puede procesar cada matriculación al vuelo.

```bash
python matriculaciones_stream_print.py "2023-10"
python matriculaciones_stream_print.py "2023-06-09"
```

## Changelog

- 0.0.2:
  - Fix: corrección en descarga de matriculaciones por mes (añadido nuevo viewstate)
  - Fix: corrección en descarga de matriculaciones por día
  - Fix: no ignorar matriculaciones sin bastidor al parsear
- 0.0.1:
  - Versión inicial: descarga y parseo de matriculaciones

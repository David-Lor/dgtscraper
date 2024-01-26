# Python DGT Scraper

**Utilidad para descargar y parsear [datasets de matriculaciones de la Dirección General de Tráfico](https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/subcategoria.faces)**

## Matriculaciones

### Descargar

El script [matriculaciones_download](matriculaciones_download.py) descarga y extrae el dataset de matriculaciones, tal y como se presenta en el [portal de microdatos](https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/subcategoria.faces).
Es necesario indicarle un mes del que descargar datos.

```bash
python matriculaciones_download.py "año-mes" --output="archivo-salida (opcional)"

# Ejemplos:
python matriculaciones_download.py "2023-01"
python matriculaciones_download.py "2023-10" --output="/home/yo/Descargas/2023-Octubre.txt"

# Si no se indica archivo de salida, se descargará en: "./matriculaciones-{año}-{mes}.txt".
# Si se indica un directorio, se creará el archivo en ese directorio.
```

El archivo de salida es un fichero de texto, con codificación iso-8859-1, donde cada línea (excepto la primera) corresponde a una matriculación.
Las columnas tienen [formato de ancho fijo](https://www.ibm.com/docs/es/baw/19.x?topic=formats-fixed-width-format) ([documentación](https://sedeapl.dgt.gob.es/IEST_INTER/pdfs/disenoRegistro/vehiculos/matriculaciones/MATRICULACIONES_MATRABA.pdf)).

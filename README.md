# Mapa de amigas de sumar

Consiste en un mapa (index.html) que carga los datos de data/data-geocoded.csv, y un script de python (main.py) para a partir de un csv con direcciones sacar la geoposición (un poco aleatorizada)

## Actualizar datos manualmente

Para actualizar los datos basta con modificar el archivo data/data-geocoded.csv.

Los cambios se publican automáticamente en saigesp.github.io/mapa-amigas-sumar/

## Generar datos a partir del script de python main.py

> Hace falta una clave de google maps (env var GOOGLE_MAPS_API_KEY)

El proceso está pensado para tener dos archivos csv con direcciones y código del formulario de action network: `data-raw-replace.csv` y `data-raw-add.csv`, el primero para reemplazar filas y el segundo para añadir filas.

El proceso geocodifica (saca latitud y longitud de la dirección) y luego la aleatoriza un poco para que no sea 100% precisa (para anonimizarla).

Los archivos `data/data-raw-replace.csv` y `data/data-raw-add.csv` están puestos en el gitignore.

**Este repositorio es público, NO SUBIR DATOS SENSIBLES**

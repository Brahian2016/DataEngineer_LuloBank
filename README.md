# DataEngineer_LuloBank

# Proyecto TV Series Analysis

Este es un proyecto de análisis de series de televisión utilizando Python y diversas bibliotecas. El objetivo principal del proyecto es obtener información sobre series de televisión, limpiar los datos, realizar análisis exploratorio y generar informes.

## Estructura del Proyecto

El proyecto está organizado en los siguientes archivos y carpetas:

- `main.py`: El archivo principal que ejecuta el flujo principal del proyecto, obteniendo información de series, limpiando datos, generando informes y realizando operaciones de agregación.

- `utils.py`: Contiene funciones útiles para obtener datos de series, normalizar datos, limpiar datos, generar informes y realizar operaciones de agregación.

- `unit_testing.py`: Archivo de pruebas unitarias para verificar el funcionamiento correcto de las funciones en `utils.py`.

- `data/`: Carpeta que contiene los archivos CSV y Parquet resultantes de la extracción y limpieza de datos.

- `json/`: Carpeta donde se guardan los archivos JSON descargados de la API.

- `profiling/`: Carpeta donde se almacenan los informes en formato PDF con el perfil de los datos.

- `db/`: Carpeta donde se encuentra la base de datos SQLite utilizada para almacenar los datos.

## Instrucciones de Uso

1. Instala las dependencias del proyecto ejecutando el siguiente comando en tu terminal:

- pip install -r requirements.txt


2. Ejecuta el archivo `main.py` para realizar el análisis y generación de informes:

- python main.py


3. Ejecuta las pruebas unitarias en el archivo `unit_testing.py` para verificar el funcionamiento correcto de las funciones:

- python unit_testing.py


## Notas

- Asegúrate de tener un entorno virtual activado antes de instalar las dependencias y ejecutar el proyecto.

- El proyecto utiliza la API de TVMaze para obtener información sobre series de televisión. Asegúrate de tener una conexión a Internet activa para que el proyecto funcione correctamente.

- Los resultados del análisis y las operaciones de agregación se mostrarán en la consola al ejecutar `main.py`.

- Los informes generados en formato PDF se almacenarán en la carpeta `profiling/`.



# Tarea-1-Sistemas-Distribuidos

Este proyecto está organizado en dos carpetas principales:

1. **Scraper**: Contiene un script que realiza scraping de datos desde Waze. Este script extrae información relevante y genera un archivo de salida llamado `alertas.json`, que contiene las alertas recopiladas.

2. **Servidor**: Incluye un servidor que consume el archivo `alertas.json` generado por el scraper y lo utiliza para procesar o mostrar los datos.

Además, el proyecto incluye un archivo `docker-compose.yml` que configura y levanta un contenedor con **mongo-express**, una herramienta para visualizar y gestionar los datos almacenados en MongoDB. Esto permite inspeccionar fácilmente los datos procesados por el servidor.

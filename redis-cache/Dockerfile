# Usa la imagen oficial de Python
FROM python:3.9-slim

# Instalar Redis
RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

# Copiar el archivo cache.py a la imagen
COPY cache.py /usr/src/app/cache.py

# Establecer el directorio de trabajo
WORKDIR /usr/src/app

# Instalar las dependencias de Python
RUN pip install pymongo redis

# Ejecutar el script cache.py al iniciar el contenedor
CMD ["python", "cache.py"]

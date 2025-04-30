# Usar una imagen base de Python 3.9 slim
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copiar el script y otros archivos necesarios al contenedor
COPY generator.py . 

# Si tienes un archivo requirements.txt, descomenta esta línea:
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Actualizar pip (opcional, para asegurarse de que esté actualizado)
RUN pip install --upgrade pip

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir requests numpy scipy

# Exponer puertos si es necesario (por ejemplo, si hay un backend HTTP)
# EXPOSE 5000

# Ejecutar el script cuando el contenedor se inicie
CMD ["python", "generator.py"]

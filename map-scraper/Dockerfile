FROM python:3.9-slim

# Instalación de dependencias del sistema
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno necesarias para headless
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Copiar archivos
WORKDIR /app
COPY requirements.txt .   
COPY scraper.py .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el scraper
CMD ["python", "scraper.py"]


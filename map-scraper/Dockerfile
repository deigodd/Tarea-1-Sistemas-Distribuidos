FROM python:3.9-buster

# Instalar dependencias necesarias para Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xdg-utils \
    libx11-dev \
    libxkbfile-dev \
    libsecret-1-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libxtst6 \
    python3-dev \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libvulkan1 \
    libxdamage1 \
    libxkbcommon0 \
    fonts-liberation \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Instalar las dependencias de Python necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del script al contenedor
COPY . /app

# Descargar e instalar ChromeDriver (el mismo que es compatible con tu versión de Chrome)
RUN wget https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Comando por defecto para ejecutar el script
CMD ["python", "scraper.py"]

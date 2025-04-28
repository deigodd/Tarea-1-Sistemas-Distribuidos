FROM python:3.9-slim

RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

COPY cache.py /usr/src/app/cache.py

WORKDIR /usr/src/app

RUN pip install pymongo redis

CMD ["python", "cache.py"]

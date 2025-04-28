FROM python:3.9-slim

WORKDIR /usr/src/app

COPY generator.py .

RUN pip install redis

CMD ["python", "generator.py"]

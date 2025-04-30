FROM python:3.9-slim

WORKDIR /usr/src/app

COPY generator.py .

RUN pip install --no-cache-dir requests numpy

CMD ["python", "generator.py"]

# clickstream_producer/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

# Default command (overridden in docker-compose)
CMD ["python", "producer.py"]

FROM python:3.11-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apt-get update && apt-get install -y curl netcat-openbsd && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root



COPY . .

CMD ["bash", "-c", "\
    echo '⏳ Waiting for Kafka at kafka:9092...' && \
    while ! nc -z kafka 9092; do sleep 1; done && \
    echo '✅ Kafka is up! Running create_topic.py...' && \
    python create_topic.py \
"]

# topic_admin/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy only poetry.lock and pyproject.toml first (to cache dependency install)
COPY poetry.lock pyproject.toml ./

# Install system dependencies & Poetry only once (cached unless you change above lines)
RUN apt-get update && apt-get install -y curl netcat-openbsd && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root



# Now copy your full code
COPY . .

CMD ["bash", "-c", "\
    echo '⏳ Waiting for Kafka at kafka:9092...' && \
    while ! nc -z kafka 9092; do sleep 1; done && \
    echo '✅ Kafka is up! Running create_topic.py...' && \
    python create_topic.py \
"]

# Default command
#CMD ["python", "create_topic.py"]

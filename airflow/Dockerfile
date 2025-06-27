FROM apache/airflow:2.9.1-python3.10

# Switch to root to install system packages
USER root

# Install system dependencies and Python tools
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libsnappy-dev \
    librdkafka-dev \
    curl \
    python3-pip \
    python3-venv \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry (safe method)
RUN pip3 install poetry==1.8.2

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /opt/airflow

# Copy pyproject.toml and poetry.lock (if available)
COPY pyproject.toml poetry.lock* ./

# Avoid poetry virtualenvs (so dependencies go into Airflow Python env)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Switch back to airflow user
USER airflow

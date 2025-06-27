FROM bitnami/spark:3.3.1

# Switch to root to install packages
USER root

# Install system dependencies for Kafka and Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libsnappy-dev \
    librdkafka-dev \
    python3-pip \
    python3-venv \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/bitnami/spark/app

# Copy the app code and requirements
COPY ./airflow/dags/avro_consumer.py ./app/
COPY spark/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && pip install --default-timeout=100 -r requirements.txt

# Drop back to non-root Spark user
USER 1001

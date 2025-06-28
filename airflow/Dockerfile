# airflow/Dockerfile
FROM apache/airflow:2.9.1-python3.10

# Switch to root to install system packages
USER root

# Install system dependencies and Python tools
# Combine apt-get update and install, and clean up in a single RUN layer
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
    netcat-openbsd \
    # Clean up apt cache in the same layer to keep image size down
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory for the application files
WORKDIR /opt/airflow

# Copy requirements.txt FIRST to leverage Docker's build cache
# If only DAGs or other application files change, this layer is cached.
COPY requirements.txt ./
USER airflow
# Install Python dependencies using pip
# --no-cache-dir is recommended to prevent pip from storing downloaded packages,
# keeping the image size smaller and avoiding potential caching issues during build.
# --upgrade pip ensures pip itself is up-to-date before installing other packages.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy DAGs, plugins, etc. after dependencies are installed
# This allows caching the dependency installation layer.
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
# If you have custom scripts or utilities, copy them here too
# COPY scripts/ /opt/airflow/scripts/

# Switch back to airflow user for security
USER airflow
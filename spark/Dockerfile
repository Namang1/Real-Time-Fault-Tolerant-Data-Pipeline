FROM bitnami/spark:3.3.1

USER root

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Create working directory
WORKDIR /opt/bitnami/spark

# Copy pyproject and poetry.lock
COPY pyproject.toml poetry.lock* ./spark/

# Copy application code
COPY app/ ./app/

# Install dependencies
RUN cd spark && poetry install --no-root

# Set Spark app directory
WORKDIR /opt/bitnami/spark/app

USER 1001

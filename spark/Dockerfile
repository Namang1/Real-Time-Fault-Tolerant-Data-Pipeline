# spark/Dockerfile
# This Dockerfile builds a custom Spark image based on Bitnami Spark.
# It is used for both spark-master and spark-worker services.

FROM bitnami/spark:3.3.1

# Define the non-root user ID for Bitnami images (typically 1001)
ARG BITNAMI_UID=1001

# Switch to root to install system-level packages
USER root

# Install system dependencies.
# Keep these if your PySpark applications (e.g., those using confluent-kafka-python)
# require these headers for compilation during pip install.
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libsnappy-dev \
    librdkafka-dev \
    curl \
    python3-pip \
    build-essential \
    netcat-openbsd \
    # Clean up apt cache in the same layer to keep image size down
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory for your Spark application code within the container.
# This should be a location where the non-root user has write permissions.
WORKDIR /opt/bitnami/spark/app

# IMPORTANT: Switch to the non-root user BEFORE copying application code and installing Python packages.
# This ensures that files and installations are owned by the correct user, preventing permission issues at runtime.
USER ${BITNAMI_UID}

# Copy your PySpark application code into the image.
# Assuming 'avro_consumer.py' is your main Spark job script.
# Adjust the source path (e.g., 'spark/jobs/avro_consumer.py') to match your project structure.
COPY spark/jobs/avro_consumer.py ./avro_consumer.py

# Copy the Spark-specific Python requirements file.
# Ensure 'spark/requirements.txt' exists in your host's 'spark' directory.
COPY spark/requirements.txt ./requirements.txt

# Install Python dependencies required by your PySpark applications.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# --- ADDING ALL REQUIRED JARS DIRECTLY ---
# This method is robust for common library JARs, ensuring correct versions are fetched.
# These will be placed directly in /opt/bitnami/spark/jars/ alongside Spark's own JARs.
# Note: For Iceberg, hadoop-aws, and aws-java-sdk-bundle, using a compatible version is crucial.
# Hadoop-aws 3.3.5 is good for Spark 3.3.1. aws-java-sdk-bundle 1.12.525 is a common recent version.
# Iceberg-spark-runtime-3.3_2.12-1.4.3 matches your Spark and Scala versions.

# --- ADDING ALL REQUIRED JARS DIRECTLY ---
COPY spark/jars/ /opt/bitnami/spark/jars/


#spark-submit --master spark://spark-master:7077 --name KafkaAvroToIceberg --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/*" --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/*" --conf spark.executor.memory=4g --conf spark.executor.cores=2 --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.iceberg.type=hadoop --conf spark.sql.catalog.iceberg.warehouse=s3a://iceberg/warehouse --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 --conf spark.hadoop.fs.s3a.access.key=minioadmin --conf spark.hadoop.fs.s3a.secret.key=minioadmin --conf spark.hadoop.fs.s3a.path.style.access=true --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.defaultCatalog=iceberg /opt/bitnami/spark/app/avro_consumer.py

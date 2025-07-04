FROM bitnami/spark:3.3.1

ARG BITNAMI_UID=1001

USER root


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
    && apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /opt/bitnami/spark/app

USER ${BITNAMI_UID}

COPY spark/jobs/avro_consumer.py ./avro_consumer.py

COPY spark/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY spark/jars/ /opt/bitnami/spark/jars/


#spark-submit --master spark://spark-master:7077 --name KafkaAvroToIceberg --conf "spark.driver.extraClassPath=/opt/bitnami/spark/jars/*" --conf "spark.executor.extraClassPath=/opt/bitnami/spark/jars/*" --conf spark.executor.memory=4g --conf spark.executor.cores=2 --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.iceberg.type=hadoop --conf spark.sql.catalog.iceberg.warehouse=s3a://iceberg/warehouse --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 --conf spark.hadoop.fs.s3a.access.key=minioadmin --conf spark.hadoop.fs.s3a.secret.key=minioadmin --conf spark.hadoop.fs.s3a.path.style.access=true --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.sql.defaultCatalog=iceberg /opt/bitnami/spark/app/avro_consumer.py

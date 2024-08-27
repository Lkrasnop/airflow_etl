# Use the latest Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAG file
COPY dags/test.py ${AIRFLOW_HOME}/dags/

# Set working directory
WORKDIR ${AIRFLOW_HOME}

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port for Airflow webserver
EXPOSE 8080

# Use the entrypoint script to start Airflow
ENTRYPOINT ["/entrypoint.sh"]

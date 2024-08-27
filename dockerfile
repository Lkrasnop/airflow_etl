# Use Python 3.11.9 as the base image
FROM python:3.11.9-slim-buster

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

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

# Initialize Airflow database and create user
RUN airflow db init && \
    airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Expose port for Airflow webserver
EXPOSE 8080

# Start Airflow webserver and scheduler
CMD ["sh", "-c", "airflow webserver & airflow scheduler"]
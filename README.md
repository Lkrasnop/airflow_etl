# Airflow ETL Project
[![Airflow ETL CI/CD](https://github.com/Lkrasnop/airflow_etl/actions/workflows/main.yml/badge.svg)](https://github.com/Lkrasnop/airflow_etl/actions/workflows/main.yml)
## Overview
This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow. It extracts data from a MySQL database, performs transformations, and loads the results into a PostgreSQL database.

## Features
- Data extraction from MySQL
- Data transformation (age and BMI grouping)
- Data loading into PostgreSQL
- Automated workflow using Apache Airflow

## Prerequisites
- Python 3.11.9
- Apache Airflow
- MySQL
- PostgreSQL
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Lkrasnop/airflow_etl.git
   cd airflow_etl
   ```

2. Create and activate a virtual environment:
   ```
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up Airflow:
   ```
   export AIRFLOW_HOME=$(pwd)/airflow
   airflow db init
   airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

## Configuration

1. Update the MySQL connection details in the Airflow UI:
   - Connection Id: mysql_default
   - Connection Type: MySQL
   - Host: your_mysql_host
   - Schema: your_mysql_database
   - Login: your_mysql_username
   - Password: your_mysql_password
   - Port: 3306

2. Update the PostgreSQL connection details in the Airflow UI:
   - Connection Id: postgres_default
   - Connection Type: Postgres
   - Host: your_postgres_host
   - Schema: your_postgres_database
   - Login: your_postgres_username
   - Password: your_postgres_password
   - Port: 5432

## Usage

1. Start the Airflow webserver:
   ```
   airflow webserver --port 8080
   ```

2. In a new terminal, start the Airflow scheduler:
   ```
   airflow scheduler
   ```

3. Access the Airflow UI at `http://localhost:8080` and enable the `mysql_to_postgresql_etl` DAG.

4. The DAG will run according to its schedule, or you can trigger it manually from the Airflow UI.

## Project Structure
- `dags/`: Contains the Airflow DAG definition
- `tests/`: Unit tests for the ETL functions
- `Dockerfile`: For containerized deployment
- `requirements.txt`: Python dependencies
- `Makefile`: Automation for git operations and other tasks

## Testing
Run the unit tests with:
```
python -m unittest discover tests
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.

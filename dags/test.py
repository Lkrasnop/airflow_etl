# # import psycopg2
# # from psycopg2.extras import execute_values
# # from airflow.hooks.postgres_hook import PostgresHook
# # from airflow import DAG
# # from airflow.operators.python import PythonOperator
# # from datetime import datetime, timedelta
# # import mysql.connector
# # import pandas as pd
# # import psycopg2
# # from psycopg2.extras import execute_values

# # default_args = {
# #     'owner': 'airflow',
# #     'depends_on_past': False,
# #     'start_date': datetime(2024, 8, 25),
# #     'email_on_failure': False,
# #     'email_on_retry': False,
# #     'retries': 1,
# #     'retry_delay': timedelta(minutes=5),
# # }

# # dag = DAG(
# #     'mysql_to_postgresql_etl',
# #     default_args=default_args,
# #     description='ETL process from MySQL to PostgreSQL',
# #     schedule_interval=timedelta(days=1),
# # )

# # def extract():
# #     connection = mysql.connector.connect(
# #         host='127.0.0.1',
# #         port=3306,
# #         user='root',
# #         password='za12zaZA12!@',
# #         database='zchema'
# #     )
# #     query = "SELECT * FROM zchema.dataset"
# #     df = pd.read_sql(query, connection)
# #     connection.close()
# #     return df.to_json()

# # def transform(**kwargs):
# #     ti = kwargs['ti']
# #     json_data = ti.xcom_pull(task_ids='extract')
# #     df = pd.read_json(json_data)
    
# #     def get_age_group(age):
# #         if age < 18: return 'Under 18'
# #         elif 18 <= age < 30: return '18-29'
# #         elif 30 <= age < 45: return '30-44'
# #         elif 45 <= age < 60: return '45-59'
# #         else: return '60 and above'
    
# #     def get_bmi_group(bmi):
# #         if bmi < 18.5: return 'Underweight'
# #         elif 18.5 <= bmi < 25: return 'Normal'
# #         elif 25 <= bmi < 30: return 'Overweight'
# #         else: return 'Obese'
    
# #     df['age_group'] = df['age'].apply(get_age_group)
# #     df['bmi_group'] = df['bmi'].apply(get_bmi_group)
# #     return df.to_json()

# # def load(**kwargs):
# #     # Use the Airflow connection ID you configured
# #     pg_hook = PostgresHook(postgres_conn_id='postgres')
# #     conn = pg_hook.get_conn()
# #     cur = conn.cursor()
    
# #     # Your PostgreSQL operations
# #     cur.execute("SELECT 1;")
# #     result = cur.fetchone()
# #     print(f"Query result: {result}")

# #     cur.close()
# #     conn.close()

# # # def load(**kwargs):
# # #     ti = kwargs['ti']
# # #     json_data = ti.xcom_pull(task_ids='transform')
# # #     df = pd.read_json(json_data)
    
# # #     conn = psycopg2.connect(
# # #         host="localhost",
# # #         database="postgres",
# # #         user="your_postgres_user",
# # #         password="your_postgres_password"
# # #     )
# # #     cur = conn.cursor()
    
# #     # Create table if not exists
# #     create_table_query = """
# #     CREATE TABLE IF NOT EXISTS test.transformed_data3 (
# #         id SERIAL PRIMARY KEY,
# #         -- Add other columns based on your DataFrame
# #         age INTEGER,
# #         bmi FLOAT,
# #         age_group VARCHAR(20),
# #         bmi_group VARCHAR(20)
# #         -- Add other columns as needed
# #     )
# #     """
# #     cur.execute(create_table_query)
    
# #     # Insert data
# #     insert_query = "INSERT INTO test.transformed_data3 (age, bmi, age_group, bmi_group) VALUES %s"
# #     values = [tuple(row) for row in df[['age', 'bmi', 'age_group', 'bmi_group']].values]
# #     execute_values(cur, insert_query, values)
    
# #     conn.commit()
# #     cur.close()
# #     conn.close()
    
# #     print(f"Data successfully loaded into PostgreSQL test.transformed_data3 table")

# # extract_task = PythonOperator(
# #     task_id='extract',
# #     python_callable=extract,
# #     dag=dag,
# # )

# # transform_task = PythonOperator(
# #     task_id='transform',
# #     python_callable=transform,
# #     dag=dag,
# # )

# # load_task = PythonOperator(
# #     task_id='load',
# #     python_callable=load,
# #     dag=dag,
# # )

# # extract_task >> transform_task >> load_task

# import psycopg2
# from psycopg2.extras import execute_values
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# import mysql.connector
# import pandas as pd
# import json
# from io import StringIO

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 8, 25),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# dag = DAG(
#     'mysql_to_postgresql_etl',
#     default_args=default_args,
#     description='ETL process from MySQL to PostgreSQL',
#     schedule_interval=timedelta(days=1),
# )

# def extract():
#     try:
#         connection = mysql.connector.connect(
#             host='127.0.0.1',
#             port=3306,
#             user='root',
#             password='za12zaZA12!@',
#             database='zchema'
#         )
#         query = "SELECT * FROM zchema.dataset"
#         df = pd.read_sql(query, connection)
#         connection.close()
        
#         print("Extracted data:")
#         print(df.head())
#         print(f"Total rows extracted: {len(df)}")
        
#         return df.to_json()
#     except Exception as e:
#         print(f"Error in extract task: {str(e)}")
#         raise

# def transform(**kwargs):
#     try:
#         ti = kwargs['ti']
#         json_data = ti.xcom_pull(task_ids='extract')
#         if not json_data:
#             raise ValueError("No data received from extract task")
#         df = pd.read_json(StringIO(json_data))
        
#         def get_age_group(age):
#             if age < 18: return 'Under 18'
#             elif 18 <= age < 30: return '18-29'
#             elif 30 <= age < 45: return '30-44'
#             elif 45 <= age < 60: return '45-59'
#             else: return '60 and above'
        
#         def get_bmi_group(bmi):
#             if bmi < 18.5: return 'Underweight'
#             elif 18.5 <= bmi < 25: return 'Normal'
#             elif 25 <= bmi < 30: return 'Overweight'
#             else: return 'Obese'
        
#         df['age_group'] = df['age'].apply(get_age_group)
#         df['bmi_group'] = df['bmi'].apply(get_bmi_group)
        
#         print("Transformed data:")
#         print(df.head())
#         print(f"Total rows transformed: {len(df)}")
        
#         return df.to_json()
#     except Exception as e:
#         print(f"Error in transform task: {str(e)}")
#         raise

# def load(**kwargs):
#     try:
#         ti = kwargs['ti']
#         json_data = ti.xcom_pull(task_ids='transform')
#         if not json_data:
#             raise ValueError("No data received from transform task")
#         df = pd.read_json(StringIO(json_data))
        
#         pg_hook = PostgresHook(postgres_conn_id='postgres')
#         conn = pg_hook.get_conn()
#         cur = conn.cursor()
        
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS transformed_data6 (
#             id SERIAL PRIMARY KEY,
#             age INTEGER,
#             bmi FLOAT,
#             age_group VARCHAR(20),
#             bmi_group VARCHAR(20)
#         )
#         """
#         cur.execute(create_table_query)
        
#         insert_query = "INSERT INTO transformed_data6 (age, bmi, age_group, bmi_group) VALUES %s"
#         values = [tuple(row) for row in df[['age', 'bmi', 'age_group', 'bmi_group']].values]
#         execute_values(cur, insert_query, values)

#         conn.commit()

#         cur.execute("SELECT * FROM transformed_data6 LIMIT 5")
#         sample_data = cur.fetchall()
#         print("Sample of uploaded data:")
#         for row in sample_data:
#             print(row)

#         cur.execute("SELECT COUNT(*) FROM transformed_data6")
#         count = cur.fetchone()[0]
#         print(f"Total rows uploaded to PostgreSQL: {count}")

#         cur.close()
#         conn.close()
        
#         print(f"Data successfully loaded into PostgreSQL transformed_data6 table")
#     except Exception as e:
#         print(f"Error in load task: {str(e)}")
#         raise

# extract_task = PythonOperator(
#     task_id='extract',
#     python_callable=extract,
#     dag=dag,
# )

# transform_task = PythonOperator(
#     task_id='transform',
#     python_callable=transform,
#     dag=dag,
# )

# load_task = PythonOperator(
#     task_id='load',
#     python_callable=load,
#     dag=dag,
# )

# extract_task >> transform_task >> load_task

# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.mysql.hooks.mysql import MySqlHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from datetime import datetime, timedelta
# import pandas as pd
# from io import StringIO
# import json

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 8, 25),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# dag = DAG(
#     'mysql_to_postgresql_etl',
#     default_args=default_args,
#     description='ETL process from MySQL to PostgreSQL',
#     schedule_interval=timedelta(days=1),
#     catchup=False,
# )

# def extract(**kwargs):
#     try:
#         mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
#         query = "SELECT * FROM dataset"  # Removed 'zchema.' as it's specified in the connection
#         df = mysql_hook.get_pandas_df(sql=query)

#         print("Extracted data:")
#         print(df.head())
#         print(f"Total rows extracted: {len(df)}")

#         return df.to_json()
#     except Exception as e:
#         print(f"Error in extract task: {str(e)}")
#         print(f"MySQL Connection Info: {mysql_hook.get_connection(mysql_hook.mysql_conn_id).get_uri()}")
#         raise

# def transform(**kwargs):
#     try:
#         ti = kwargs['ti']
#         json_data = ti.xcom_pull(task_ids='extract')
#         if not json_data:
#             raise ValueError("No data received from extract task")
#         df = pd.read_json(StringIO(json_data))

#         def get_age_group(age):
#             if age < 18: return 'Under 18'
#             elif 18 <= age < 30: return '18-29'
#             elif 30 <= age < 45: return '30-44'
#             elif 45 <= age < 60: return '45-59'
#             else: return '60 and above'

#         def get_bmi_group(bmi):
#             if bmi < 18.5: return 'Underweight'
#             elif 18.5 <= bmi < 25: return 'Normal'
#             elif 25 <= bmi < 30: return 'Overweight'
#             else: return 'Obese'

#         df['age_group'] = df['age'].apply(get_age_group)
#         df['bmi_group'] = df['bmi'].apply(get_bmi_group)

#         print("Transformed data:")
#         print(df.head())
#         print(f"Total rows transformed: {len(df)}")

#         return df.to_json()
#     except Exception as e:
#         print(f"Error in transform task: {str(e)}")
#         raise

# def load(**kwargs):
#     try:
#         ti = kwargs['ti']
#         json_data = ti.xcom_pull(task_ids='transform')
#         if not json_data:
#             raise ValueError("No data received from transform task")
#         df = pd.read_json(StringIO(json_data))

#         pg_hook = PostgresHook(postgres_conn_id='postgres_default')
#         conn = pg_hook.get_conn()
#         cur = conn.cursor()

#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS transformed_data6 (
#             id SERIAL PRIMARY KEY,
#             age INTEGER,
#             bmi FLOAT,
#             age_group VARCHAR(20),
#             bmi_group VARCHAR(20)
#         )
#         """
#         cur.execute(create_table_query)

#         pg_hook.insert_rows(
#             table='transformed_data6',
#             rows=df[['age', 'bmi', 'age_group', 'bmi_group']].values.tolist(),
#             target_fields=['age', 'bmi', 'age_group', 'bmi_group']
#         )

#         cur.execute("SELECT * FROM transformed_data6 LIMIT 5")
#         sample_data = cur.fetchall()
#         print("Sample of uploaded data:")
#         for row in sample_data:
#             print(row)

#         cur.execute("SELECT COUNT(*) FROM transformed_data6")
#         count = cur.fetchone()[0]
#         print(f"Total rows uploaded to PostgreSQL: {count}")

#         cur.close()
#         conn.close()

#         print(f"Data successfully loaded into PostgreSQL transformed_data6 table")
#     except Exception as e:
#         print(f"Error in load task: {str(e)}")
#         raise

# extract_task = PythonOperator(
#     task_id='extract',
#     python_callable=extract,
#     dag=dag,
# )

# transform_task = PythonOperator(
#     task_id='transform',
#     python_callable=transform,
#     dag=dag,
# )

# load_task = PythonOperator(
#     task_id='load',
#     python_callable=load,
#     dag=dag,
# )

# extract_task >> transform_task >> load_task


from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
from io import StringIO
import json
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_to_postgresql_etl',
    default_args=default_args,
    description='ETL process from MySQL to PostgreSQL',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

def extract(**kwargs):
    try:
        mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
        conn_details = mysql_hook.get_connection(mysql_hook.mysql_conn_id)
        print(f"Attempting to connect to MySQL at {conn_details.host}:{conn_details.port}")
        
        query = "SELECT * FROM dataset"
        df = mysql_hook.get_pandas_df(sql=query)

        print("Extracted data:")
        print(df.head())
        print(f"Total rows extracted: {len(df)}")

        return df.to_json()
    except Exception as e:
        print(f"Error in extract task: {str(e)}")
        print(f"MySQL Connection Info: {mysql_hook.get_connection(mysql_hook.mysql_conn_id).get_uri()}")
        raise

def transform(**kwargs):
    try:
        ti = kwargs['ti']
        json_data = ti.xcom_pull(task_ids='extract')
        if not json_data:
            raise ValueError("No data received from extract task")
        df = pd.read_json(StringIO(json_data))

        def get_age_group(age):
            if age < 18: return 'Under 18'
            elif 18 <= age < 30: return '18-29'
            elif 30 <= age < 45: return '30-44'
            elif 45 <= age < 60: return '45-59'
            else: return '60 and above'

        def get_bmi_group(bmi):
            if bmi < 18.5: return 'Underweight'
            elif 18.5 <= bmi < 25: return 'Normal'
            elif 25 <= bmi < 30: return 'Overweight'
            else: return 'Obese'

        df['age_group'] = df['age'].apply(get_age_group)
        df['bmi_group'] = df['bmi'].apply(get_bmi_group)

        print("Transformed data:")
        print(df.head())
        print(f"Total rows transformed: {len(df)}")

        return df.to_json()
    except Exception as e:
        print(f"Error in transform task: {str(e)}")
        raise

def load(**kwargs):
    try:
        ti = kwargs['ti']
        json_data = ti.xcom_pull(task_ids='transform')
        if not json_data:
            raise ValueError("No data received from transform task")
        df = pd.read_json(StringIO(json_data))

        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        conn = pg_hook.get_conn()
        cur = conn.cursor()

        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transformed_data6 (
            id SERIAL PRIMARY KEY,
            age INTEGER,
            bmi FLOAT,
            age_group VARCHAR(20),
            bmi_group VARCHAR(20)
        )
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'transformed_data6' created or already exists.")

        # Check if table was created successfully
        cur.execute("SELECT to_regclass('public.transformed_data6')")
        if cur.fetchone()[0] is None:
            raise Exception("Table 'transformed_data6' was not created successfully")

        # Insert data
        insert_query = """
        INSERT INTO transformed_data6 (age, bmi, age_group, bmi_group)
        VALUES (%s, %s, %s, %s)
        """
        values = df[['age', 'bmi', 'age_group', 'bmi_group']].values.tolist()
        cur.executemany(insert_query, values)
        conn.commit()

        print(f"Inserted {len(values)} rows into 'transformed_data6'")

        # Verify data
        cur.execute("SELECT * FROM transformed_data6 LIMIT 5")
        sample_data = cur.fetchall()
        print("Sample of uploaded data:")
        for row in sample_data:
            print(row)

        cur.execute("SELECT COUNT(*) FROM transformed_data6")
        count = cur.fetchone()[0]
        print(f"Total rows in transformed_data6: {count}")

        cur.close()
        conn.close()

        print(f"Data successfully loaded into PostgreSQL transformed_data6 table")
    except Exception as e:
        print(f"Error in load task: {str(e)}")
        print(f"PostgreSQL Connection Info: {pg_hook.get_connection(pg_hook.postgres_conn_id).get_uri()}")
        raise

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
)

extract_task >> transform_task >> load_task
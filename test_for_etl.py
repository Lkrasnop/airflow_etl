import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from io import StringIO
import sys

# Mock Airflow modules
sys.modules['airflow'] = MagicMock()
sys.modules['airflow.operators.python'] = MagicMock()
sys.modules['airflow.providers.mysql.hooks.mysql'] = MagicMock()
sys.modules['airflow.providers.postgres.hooks.postgres'] = MagicMock()

# Now import your functions
from test import extract, transform, load
# from dags.test import extract, transform, load

class MockMySqlHook:
    def __init__(self, mysql_conn_id):
        self.mysql_conn_id = mysql_conn_id

    def get_connection(self, conn_id):
        mock_conn = MagicMock()
        mock_conn.host = 'localhost'
        mock_conn.port = 3306
        return mock_conn

    def get_pandas_df(self, sql):
        return pd.DataFrame({
            'age': [25, 30, 35],
            'bmi': [22.5, 24.0, 26.5]
        })

class MockPostgresHook:
    def __init__(self, postgres_conn_id):
        self.postgres_conn_id = postgres_conn_id

    def get_conn(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn

class TestETLProcess(unittest.TestCase):

    @patch('test.MySqlHook', MockMySqlHook)
    def test_extract(self):
        result = extract()
        df = pd.read_json(StringIO(result))
        self.assertEqual(len(df), 3)
        self.assertTrue('age' in df.columns)
        self.assertTrue('bmi' in df.columns)

    def test_transform(self):
        mock_ti = MagicMock()
        mock_ti.xcom_pull.return_value = pd.DataFrame({
            'age': [25, 30, 35],
            'bmi': [22.5, 24.0, 26.5]
        }).to_json()

        result = transform(ti=mock_ti)
        df = pd.read_json(StringIO(result))
        
        self.assertTrue('age_group' in df.columns)
        self.assertTrue('bmi_group' in df.columns)
        self.assertEqual(list(df['age_group']), ['18-29', '30-44', '30-44'])
        self.assertEqual(list(df['bmi_group']), ['Normal', 'Normal', 'Overweight'])

    @patch('test.PostgresHook', MockPostgresHook)
    def test_load(self):
        mock_ti = MagicMock()
        mock_ti.xcom_pull.return_value = pd.DataFrame({
            'age': [25, 30, 35],
            'bmi': [22.5, 24.0, 26.5],
            'age_group': ['18-29', '30-44', '30-44'],
            'bmi_group': ['Normal', 'Normal', 'Overweight']
        }).to_json()

        # This should run without raising an exception
        load(ti=mock_ti)

if __name__ == '__main__':
    unittest.main()
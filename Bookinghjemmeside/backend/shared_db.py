import os
import pyodbc

def get_connection():
    server = os.environ['SQL_SERVER']
    database = os.environ['SQL_DB']
    username = os.environ['SQL_USER']
    password = os.environ['SQL_PASSWORD']

    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    conn = pyodbc.connect(conn_str)
    return conn

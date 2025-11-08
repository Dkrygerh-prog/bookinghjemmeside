import pyodbc

def get_connection():
    server = 'bookinghjemmeside.database.windows.net'
    database = 'bookingdb'
    username = 'dkrygerh'
    password = 'D3nnisSQL#2024'
    driver= '{ODBC Driver 17 for SQL Server}'
    
    conn = pyodbc.connect(
        'DRIVER='+driver+
        ';SERVER='+server+
        ';PORT=1433;DATABASE='+database+
        ';UID='+username+
        ';PWD='+password
    )
    return conn

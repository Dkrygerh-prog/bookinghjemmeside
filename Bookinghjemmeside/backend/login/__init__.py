import azure.functions as func
import json
from shared_db import get_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    username = req.params.get('username')
    password = req.params.get('password')

    if not username or not password:
        return func.HttpResponse("Manglende brugernavn eller kode", status_code=400)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT UserID FROM Users WHERE Username=? AND Password=?", username, password)
    row = cursor.fetchone()
    conn.close()

    if row:
        return func.HttpResponse(json.dumps({"UserID": row[0]}), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse("Forkert brugernavn eller kode", status_code=401)

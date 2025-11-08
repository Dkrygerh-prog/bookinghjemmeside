import azure.functions as func
import json
from datetime import datetime, timedelta
from shared_db import get_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        user_id = data['UserID']
        room = data['Room']
        start_time = datetime.fromisoformat(data['StartTime'])
        end_time = start_time + timedelta(hours=2)
    except:
        return func.HttpResponse("Ugyldigt data", status_code=400)

    conn = get_connection()
    cursor = conn.cursor()

    # Tjek om slot er ledigt
    cursor.execute("SELECT COUNT(*) FROM Bookings WHERE Room=? AND NOT (EndTime <= ? OR StartTime >= ?)", room, start_time, end_time)
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return func.HttpResponse("Slot er allerede booket", status_code=409)

    # Book
    cursor.execute("INSERT INTO Bookings (UserID, Room, StartTime, EndTime) VALUES (?, ?, ?, ?)", user_id, room, start_time, end_time)
    conn.commit()
    conn.close()

    return func.HttpResponse("Booking succesfuld", status_code=201)

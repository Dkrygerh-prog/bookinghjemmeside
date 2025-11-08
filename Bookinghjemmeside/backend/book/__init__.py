import azure.functions as func
import json
from common import get_connection
from datetime import datetime, timedelta

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        user_id = data['UserID']
        room = data['Room']
        start_time = datetime.fromisoformat(data['StartTime'])
        end_time = start_time + timedelta(hours=2)
    except Exception as e:
        return func.HttpResponse(f"Fejl i data: {str(e)}", status_code=400)

    conn = get_connection()
    cursor = conn.cursor()
    # Check overlap
    cursor.execute("""
        SELECT COUNT(*) FROM Bookings
        WHERE Room=? AND NOT (EndTime<=? OR StartTime>=?)
    """, room, start_time, end_time)
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return func.HttpResponse("Tidspunkt allerede booket", status_code=409)

    cursor.execute("INSERT INTO Bookings (UserID, Room, StartTime, EndTime) VALUES (?,?,?,?)",
                   user_id, room, start_time, end_time)
    conn.commit()
    conn.close()
    return func.HttpResponse("Booking oprettet", status_code=201)

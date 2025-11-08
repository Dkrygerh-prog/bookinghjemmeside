import azure.functions as func
import json
from datetime import datetime, timedelta
from shared_db import get_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    week_start = req.params.get('week_start')
    if not week_start:
        return func.HttpResponse("Manglende week_start", status_code=400)

    start_date = datetime.fromisoformat(week_start)
    end_date = start_date + timedelta(days=7)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BookingID, UserID, Room, StartTime, EndTime FROM Bookings WHERE StartTime BETWEEN ? AND ?", start_date, end_date)
    bookings = [{"BookingID": row[0], "UserID": row[1], "Room": row[2], "StartTime": row[3].isoformat(), "EndTime": row[4].isoformat()} for row in cursor.fetchall()]
    conn.close()

    return func.HttpResponse(json.dumps(bookings), mimetype="application/json", status_code=200)

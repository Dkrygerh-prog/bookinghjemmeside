import azure.functions as func
import json
from common import get_connection
from datetime import datetime, timedelta

def main(req: func.HttpRequest) -> func.HttpResponse:
    week_start_str = req.params.get('week_start')  # format: YYYY-MM-DD
    if not week_start_str:
        return func.HttpResponse("Manglende week_start parameter", status_code=400)

    week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
    week_end = week_start + timedelta(days=7)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT BookingID, UserID, Room, StartTime, EndTime
        FROM Bookings
        WHERE StartTime >= ? AND StartTime < ?
    """, week_start, week_end)

    rows = cursor.fetchall()
    bookings = []
    for row in rows:
        bookings.append({
            "BookingID": row[0],
            "UserID": row[1],
            "Room": row[2],
            "StartTime": row[3].isoformat(),
            "EndTime": row[4].isoformat()
        })
    conn.close()

    return func.HttpResponse(json.dumps(bookings), mimetype="application/json")

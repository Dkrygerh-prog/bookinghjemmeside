import azure.functions as func
from common import get_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        booking_id = int(req.params.get('BookingID'))
    except:
        return func.HttpResponse("Manglende eller forkert BookingID", status_code=400)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Bookings WHERE BookingID=?", booking_id)
    conn.commit()
    conn.close()
    return func.HttpResponse("Booking annulleret", status_code=200)

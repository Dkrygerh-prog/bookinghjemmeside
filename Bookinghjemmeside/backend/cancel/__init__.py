import azure.functions as func
from shared_db import get_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    booking_id = req.params.get('BookingID')
    if not booking_id:
        return func.HttpResponse("Manglende BookingID", status_code=400)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Bookings WHERE BookingID=?", booking_id)
    conn.commit()
    conn.close()

    return func.HttpResponse("Booking annulleret", status_code=200)

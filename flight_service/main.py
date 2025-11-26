# flight_service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from .flight_logic import get_available_dates, get_seat_status, perform_booking, perform_cancellation

# --- FastAPI App Setup ---
app = FastAPI(
    title="FlightBookingService", 
    description="Microservice handling all flight inventory and bookings."
)

# --- Schemas for POST requests (Data must match ADK RemoteTool schema) ---
class BookingData(BaseModel):
    date: str
    seat_id: str
    customer: dict

class CancelData(BaseModel):
    booking_id: str

# --- Endpoints (Called by the ADK Remote Tools) ---

@app.get("/dates")
def dates_endpoint():
    """Returns available flight dates."""
    return {"dates": get_available_dates()}

@app.get("/seats/{date}")
def seats_endpoint(date: str):
    """Returns available seats for a specific date."""
    return get_seat_status(date)

@app.post("/book")
def book_endpoint(data: BookingData):
    """Processes a flight seat booking request."""
    return perform_booking(data.date, data.seat_id, data.customer)

@app.post("/cancel")
def cancel_endpoint(data: CancelData):
    """Processes a flight booking cancellation request."""
    return perform_cancellation(data.booking_id)

# --- EXECUTION NOTE ---
# To run this service, navigate to the flight_service directory and execute:
# uvicorn main:app --host 0.0.0.0 --port 8002
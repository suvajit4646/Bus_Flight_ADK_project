# bus_service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from .bus_logic import get_available_dates, get_seat_status, perform_booking, perform_cancellation

app = FastAPI()

# --- Schemas for POST requests ---
class BookingData(BaseModel):
    date: str
    seat_id: str
    customer: dict

class CancelData(BaseModel):
    booking_id: str

# --- Endpoints (Must match ADK RemoteTool URLs) ---

@app.get("/dates")
def dates_endpoint():
    """Maps to tool_bus_get_dates (GET)"""
    return {"dates": get_available_dates()}

@app.get("/seats/{date}")
def seats_endpoint(date: str):
    """Maps to tool_bus_check_seats (GET)"""
    return get_seat_status(date)

@app.post("/book")
def book_endpoint(data: BookingData):
    """Maps to tool_bus_book (POST)"""
    return perform_booking(data.date, data.seat_id, data.customer)

@app.post("/cancel")
def cancel_endpoint(data: CancelData):
    """Maps to tool_bus_cancel (POST)"""
    return perform_cancellation(data.booking_id)

# How to Run: uvicorn bus_service.main:app --host 0.0.0.0 --port 8001
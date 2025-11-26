# flight_service/flight_logic.py
import os
import json
from datetime import datetime, timedelta
import random
import string

# --- Configuration ---
FLIGHT_DB_FILE = "flight_database.json" 

# --- Shared Helper Functions ---

def generate_id(prefix="FL"):
    """Generate a unique ID like 'FL-ABC123'"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}-{numbers}{letters}" # Changed order slightly for differentiation

def get_valid_dates():
    """Generate next 7 days excluding Sunday"""
    valid_dates = []
    current_date = datetime.now()
    days_added = 0
    while len(valid_dates) < 7:
        check_date = current_date + timedelta(days=days_added)
        if check_date.weekday() != 6:  # 6 = Sunday
            valid_dates.append(check_date.strftime("%Y-%m-%d"))
        days_added += 1
    return valid_dates

def initialize_flight_database():
    """Initialize the flight database"""
    seats = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    if not os.path.exists(FLIGHT_DB_FILE):
        database = {}
        for date in get_valid_dates():
            database[date] = {}
            for seat in seats:
                database[date][seat] = {
                    "status": "available",
                    "customer": None,
                    "booking_id": None
                }
        with open(FLIGHT_DB_FILE, 'w') as f:
            json.dump(database, f, indent=4)
        print(f"[System]: Flight Database initialized.")

# --- Generic Database Logic ---

def get_available_dates():
    try:
        with open(FLIGHT_DB_FILE, 'r') as f:
            database = json.load(f)
        return list(database.keys())
    except Exception:
        return []

def get_seat_status(date: str):
    try:
        with open(FLIGHT_DB_FILE, 'r') as f:
            database = json.load(f)
        if date not in database:
            return {"count": 0, "ids": []}
        
        available = [sid for sid, det in database[date].items() if det["status"] == "available"]
        return {"count": len(available), "ids": available}
    except Exception:
        return {"count": 0, "ids": []}

def perform_booking(date: str, seat_id: str, customer: dict):
    seat_id = seat_id.upper().strip()
    try:
        with open(FLIGHT_DB_FILE, 'r') as f:
            database = json.load(f)
        
        if date not in database or seat_id not in database[date]:
            return {"success": False, "message": "Invalid date or seat."}
            
        if database[date][seat_id]["status"] != "available":
            return {"success": False, "message": "Seat already occupied."}
            
        booking_id = generate_id("FL") # Uses FL prefix
        database[date][seat_id].update({
            "status": "occupied",
            "customer": customer,
            "booking_id": booking_id
        })
        
        with open(FLIGHT_DB_FILE, 'w') as f:
            json.dump(database, f, indent=4)
            
        return {"success": True, "booking_id": booking_id}
    except Exception as e:
        return {"success": False, "message": str(e)}

def perform_cancellation(booking_id: str):
    booking_id = booking_id.upper().strip()
    try:
        with open(FLIGHT_DB_FILE, 'r') as f:
            database = json.load(f)
            
        for date, seats in database.items():
            for seat_id, info in seats.items():
                if info.get("booking_id") == booking_id:
                    # Cancel
                    database[date][seat_id] = {"status": "available", "customer": None, "booking_id": None}
                    with open(FLIGHT_DB_FILE, 'w') as f:
                        json.dump(database, f, indent=4)
                    return {"success": True, "details": {"date": date, "seat": seat_id}}
                    
        return {"success": False, "message": "Booking ID not found."}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Initialize the database immediately when imported
initialize_flight_database()
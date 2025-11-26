
# travel_concierge/agent.py
import os
import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

# Load environment variables (e.g., GEMINI_API_KEY, SERVICE_URLs)
load_dotenv()

# --- 1. Service Configuration ---
BUS_BASE_URL = os.getenv("BUS_SERVICE_URL", "http://localhost:8001")
FLIGHT_BASE_URL = os.getenv("FLIGHT_SERVICE_URL", "http://localhost:8002")

# --- 2. Customer Agent (Remains Local) ---

def RemoteTool_get_customer_details(name: str, phone: str, email: str) -> dict:
    """Captures verified customer contact details."""
    return {"name": name, "phone": phone, "email": email}

customer_agent = Agent(
    name='customer_agent',
    description="Collects contact info (name, phone, email) from the user.",
    tools=[FunctionTool(RemoteTool_get_customer_details)]
)

# --- 3. Remote Tool Definitions (BUS) ---

def bus_get_dates() -> dict:
    """Get available BUS travel dates."""
    response = requests.get(f"{BUS_BASE_URL}/dates")
    response.raise_for_status()
    return response.json()

def bus_check_seats(date: str) -> dict:
    """Check available BUS seats for a specific date."""
    response = requests.get(f"{BUS_BASE_URL}/seats/{date}")
    response.raise_for_status()
    return response.json()

def bus_book(date: str, seat_id: str, customer: dict) -> dict:
    """Book a BUS seat."""
    response = requests.post(f"{BUS_BASE_URL}/book", json={"date": date, "seat_id": seat_id, "customer": customer})
    response.raise_for_status()
    return response.json()

def bus_cancel(booking_id: str) -> dict:
    """Cancel a BUS booking (ID starts with BK)."""
    response = requests.post(f"{BUS_BASE_URL}/cancel", json={"booking_id": booking_id})
    response.raise_for_status()
    return response.json()

RemoteTool_bus_get_dates = FunctionTool(bus_get_dates)
RemoteTool_bus_check_seats = FunctionTool(bus_check_seats)
RemoteTool_bus_book = FunctionTool(bus_book)
RemoteTool_bus_cancel = FunctionTool(bus_cancel)

# --- 4. Remote Tool Definitions (FLIGHT) ---

def flight_get_dates() -> dict:
    """Get available FLIGHT travel dates."""
    response = requests.get(f"{FLIGHT_BASE_URL}/dates")
    response.raise_for_status()
    return response.json()

def flight_check_seats(date: str) -> dict:
    """Check available FLIGHT seats for a specific date."""
    response = requests.get(f"{FLIGHT_BASE_URL}/seats/{date}")
    response.raise_for_status()
    return response.json()

def flight_book(date: str, seat_id: str, customer: dict) -> dict:
    """Book a FLIGHT seat."""
    response = requests.post(f"{FLIGHT_BASE_URL}/book", json={"date": date, "seat_id": seat_id, "customer": customer})
    response.raise_for_status()
    return response.json()

def flight_cancel(booking_id: str) -> dict:
    """Cancel a FLIGHT booking (ID starts with FL)."""
    response = requests.post(f"{FLIGHT_BASE_URL}/cancel", json={"booking_id": booking_id})
    response.raise_for_status()
    return response.json()

RemoteTool_flight_get_dates = FunctionTool(flight_get_dates)
RemoteTool_flight_check_seats = FunctionTool(flight_check_seats)
RemoteTool_flight_book = FunctionTool(flight_book)
RemoteTool_flight_cancel = FunctionTool(flight_cancel)

# --- 5. Agent Definitions (Using Remote RemoteTools) ---

bus_agent = Agent(
    name='bus_agent',
    description="Manages BUS bookings via external microservice.",
    tools=[RemoteTool_bus_get_dates, RemoteTool_bus_check_seats, RemoteTool_bus_book, RemoteTool_bus_cancel]
)

flight_agent = Agent(
    name='flight_agent',
    description="Manages FLIGHT bookings via external microservice.",
    tools=[RemoteTool_flight_get_dates, RemoteTool_flight_check_seats, RemoteTool_flight_book, RemoteTool_flight_cancel]
)

# 6. Root Agent (Orchestrator)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='TravelConcierge',
    sub_agents=[bus_agent, flight_agent, customer_agent],
    instruction="""
    You are a sophisticated Travel Concierge. Route requests to bus_agent or flight_agent.
    ... [Keep the original CORE FLOW and Cancellation instructions] ...
    """
)
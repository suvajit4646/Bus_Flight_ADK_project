# Travel Concierge

A sophisticated multi-agent travel booking system built with Google's ADK (Agent Development Kit) and FastAPI. This project demonstrates microservices architecture with autonomous agents handling bus and flight bookings through a unified concierge interface.

## Features

- **Intelligent Agent Orchestration**: Root agent routes requests to specialized sub-agents (bus_agent, flight_agent, customer_agent)
- **Microservices Architecture**: Separate FastAPI services for bus and flight bookings
- **Customer Management**: Collects and verifies customer contact information
- **Dynamic Booking System**: Real-time seat availability management
- **Booking Cancellation**: Support for canceling existing bookings with unique booking IDs
- **Date Management**: Automatic generation of 7-day travel windows (excluding Sundays)

## Project Structure

```
travel-concierge/
├── bus_service/
│   ├── bus_logic.py          # Bus booking logic and database operations
│   ├── main.py               # FastAPI endpoints for bus service
│   └── bus_database2.json    # Bus seat inventory database
├── flight_service/
│   ├── flight_logic.py       # Flight booking logic and database operations
│   ├── main.py               # FastAPI endpoints for flight service
│   └── flight_database.json  # Flight seat inventory database
├── agent.py                  # Multi-agent orchestration with ADK
├── __init__.py               # Package initialization
├── .env                      # Environment variables
└── README.md                 # This file
```

## Prerequisites

- Python 3.8+
- pip or conda package manager
- Google Cloud Project with ADK enabled

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-concierge.git
cd travel-concierge
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables in `.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_api_key_here
BUS_SERVICE_URL=http://localhost:8001
FLIGHT_SERVICE_URL=http://localhost:8002
```

## Running the Project

### Start the Bus Service
```bash
uvicorn bus_service.main:app --host 0.0.0.0 --port 8001
```

### Start the Flight Service
```bash
uvicorn flight_service.main:app --host 0.0.0.0 --port 8002
```

### Start the Root Agent
```bash
python -m travel_concierge
```

## API Endpoints

### Bus Service (Port 8001)

- `GET /dates` - Get available bus travel dates
- `GET /seats/{date}` - Check available seats for a specific date
- `POST /book` - Book a bus seat
- `POST /cancel` - Cancel a bus booking

### Flight Service (Port 8002)

- `GET /dates` - Get available flight travel dates
- `GET /seats/{date}` - Check available seats for a specific date
- `POST /book` - Book a flight seat
- `POST /cancel` - Cancel a flight booking

## Usage Example

```python
from travel_concierge import root_agent

# The agent will orchestrate the entire booking flow
response = root_agent.process_request(
    "I'd like to book a bus seat for tomorrow. My name is John Doe, phone is 555-1234, email is john@example.com"
)
```

## Database Structure

Both bus and flight services use JSON-based databases with the following structure:

```json
{
  "2025-11-19": {
    "A": {
      "status": "available|occupied",
      "customer": null | {...customer_info...},
      "booking_id": null | "BK-ABC123"
    },
    ...
  }
}
```

**Status Values**: `available` or `occupied`
**Booking ID Format**: `BK-XXXXXX` for bus, `FL-XXXXXX` for flights

## Key Components

### Bus Logic (`bus_logic.py`)
- Manages bus seat inventory
- Generates unique booking IDs with prefix `BK`
- Handles booking and cancellation operations
- Maintains JSON database of seat statuses

### Flight Logic (`flight_logic.py`)
- Manages flight seat inventory
- Generates unique booking IDs with prefix `FL`
- Handles booking and cancellation operations
- Maintains JSON database of seat statuses

### Agent (`agent.py`)
- **root_agent**: Main orchestrator that routes requests to sub-agents
- **bus_agent**: Handles all bus-related operations
- **flight_agent**: Handles all flight-related operations
- **customer_agent**: Collects customer contact information

## Available Dates

The system automatically generates 7 available travel dates, excluding Sundays. Dates are formatted as `YYYY-MM-DD`.

## Booking ID Format

- Bus bookings: `BK-ABC123` (3 letters + 3 numbers)
- Flight bookings: `FL-123ABC` (3 numbers + 3 letters)

## Error Handling

Both services include comprehensive error handling for:
- Invalid dates or seat IDs
- Already occupied seats
- Invalid booking IDs for cancellation
- Database file corruption

## Development

To extend the system with additional transport modes:

1. Create a new `{service}_logic.py` file following the pattern of bus_logic.py
2. Create a new `{service}/main.py` with FastAPI endpoints
3. Add new agent functions in `agent.py` and create a new sub-agent
4. Update `.env` with the new service URL

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

## Acknowledgments

- Built with [Google ADK](https://cloud.google.com/vertex-ai/docs/agent-builder)
- API framework: [FastAPI](https://fastapi.tiangolo.com/)
- Data persistence: JSON-based storage

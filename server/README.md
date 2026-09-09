# Air Vision Server

FastAPI backend service for the Air Vision project, providing real-time aircraft telemetry and geographic flight lookups powered by the open ADS-B API (`api.adsb.lol`).

---

## Overview

The Air Vision Server serves as the central API for tracking aircraft. It integrates with external flight data feeds, normalizes telemetry data into typed schemas, and exposes high-performance asynchronous endpoints for frontend consumers and services.

### Key Capabilities

- **Registration Lookup**: Fetch live telemetry for an aircraft by its tail number/registration.
- **Geographic Radius Search**: Find all active aircraft within a given distance (nautical miles) of a coordinate point (`lat`/`lon`).
- **Resilient Upstream Handling**: Managed `httpx` async sessions with custom User-Agent identification, connection pooling, and proactive timeout/rate-limit management.
- **Structured Domain Architecture**: Separation of concerns across API routing, business domain logic, typed schemas, and centralized error handling.

---

## Requirements

- **Python**: `>= 3.11` (tested with Python 3.14)
- **Virtual Environment**: `.venv/` recommended

---

## Setup & Installation

From the `server/` directory:

1. **Create and activate a virtual environment**:

   ```bash
   # macOS / Linux (bash/zsh)
   python3 -m venv .venv
   source .venv/bin/activate

   # Fish shell
   source .venv/bin/activate.fish
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   _Alternatively, install in editable mode:_
   ```bash
   pip install -e .
   ```

---

## Running Locally

Start the local development server with automatic reload:

```bash
uvicorn main:app --reload
```

- **Base API URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## CORS Configuration

Configured in `app/main.py` to allow requests from the local frontend client:

- **Allowed Origins**: `http://localhost:5173` (Vite dev server)
- **Allowed Methods**: `*`
- **Allowed Headers**: `*`
- **Credentials**: Supported

---

## Current API Endpoints

### 1. General Endpoints

| Method | Path         | Description                 | Response Model     |
| :----- | :----------- | :-------------------------- | :----------------- |
| `GET`  | `/`          | Temporary greeting endpoint | `dict`             |
| `GET`  | `/v1/health` | Service health status check | `{"status": "ok"}` |

### 2. Flight Domain Endpoints (`/v1/flights`)

| Method | Path                                        | Description                                         | Response Model               |
| :----- | :------------------------------------------ | :-------------------------------------------------- | :--------------------------- |
| `GET`  | `/v1/flights/reg/{registration}`            | Real-time telemetry for an aircraft by registration | `FlightTelemetryLight`       |
| `GET`  | `/v1/flights/point/{lat}/{lon}/{radius_nm}` | Active aircraft within a geographic radius          | `list[FlightTelemetryLight]` |

---

### Request & Response Examples

#### A. Single Aircraft Registration Lookup

```bash
curl http://127.0.0.1:8000/v1/flights/reg/G-NEOP
```

**Response (`200 OK`)**:

```json
{
  "registration": "G-NEOP",
  "aircraft_type": "A21N",
  "latitude": 51.468631,
  "longitude": -0.483532,
  "true_heading": 180.0
}
```

_If the aircraft is offline or unrecognized (`404 Not Found`):_

```json
{
  "detail": "Aircraft with registration 'G-NEOP' is not found or offline"
}
```

#### B. Geographic Point Radius Query

```bash
curl "http://127.0.0.1:8000/v1/flights/point/51.47/-0.45/10"
```

**Response (`200 OK`)**:

```json
[
  {
    "registration": "G-NEOP",
    "aircraft_type": "A21N",
    "latitude": 51.468631,
    "longitude": -0.483532,
    "true_heading": 180.0
  },
  {
    "registration": "EI-DEL",
    "aircraft_type": "A320",
    "latitude": 51.341766,
    "longitude": -0.372644,
    "true_heading": 305.74
  }
]
```

---

## Error Handling Architecture

The server adopts domain-driven exception handling. The domain layer raises typed domain exceptions that are intercepted by centralized FastAPI exception handlers in `app/api/errors.py`:

| Domain Exception         | HTTP Status                 | Detail / Meaning                                                        |
| :----------------------- | :-------------------------- | :---------------------------------------------------------------------- |
| `ADSBTimeoutError`       | `504 Gateway Timeout`       | Upstream ADS-B service exceeded the 10-second request timeout           |
| `ADSBRateLimitError`     | `429 Too Many Requests`     | Upstream ADS-B service is throttling requests                           |
| `ADSBUpstreamError`      | `502 Bad Gateway`           | Upstream network failure, 5xx server error, or invalid JSON payload     |
| `HTTPException`          | `404 Not Found`             | Requested aircraft is offline or no active planes exist in target range |
| `RequestValidationError` | `422 Unprocessable Content` | Invalid parameter types (e.g., non-numeric coordinates)                 |

All error responses strictly follow the standardized JSON structure:

```json
{
  "detail": "Error description message"
}
```

---

## Project Structure

```text
server/
├── README.md                         # Server documentation and architecture guide
├── pyproject.toml                    # Python project configuration and package dependencies
├── requirements.txt                  # Pinned environment package requirements
├── .gitignore                        # Files excluded from version control
└── app/
    ├── __init__.py                   # Marks app as a Python package
    ├── main.py                       # FastAPI application setup, CORS, router mounting
    ├── api/
    │   ├── __init__.py               # Marks API package
    │   ├── errors.py                 # Centralized exception handlers for domain errors
    │   └── v1/
    │       ├── __init__.py           # Marks v1 API package
    │       └── routes/
    │           ├── __init__.py       # Marks routes package
    │           ├── health.py         # Health-check endpoint (/v1/health)
    │           └── flights/
    │               ├── __init__.py   # Unified flights router (/v1/flights)
    │               ├── reg.py        # Registration lookup endpoint (/v1/flights/reg/{registration})
    │               └── point.py      # Geographic radius query endpoint (/v1/flights/point/{lat}/{lon}/{radius_nm})
    └── domains/
        ├── __init__.py               # Marks domain package
        └── flights/
            ├── __init__.py           # Marks flights domain package
            ├── client.py             # ADSBClient for external adsb.lol API communication
            ├── exceptions.py         # Domain-specific exceptions (Timeout, RateLimit, Upstream)
            └── schemas.py            # Pydantic telemetry models (FlightTelemetryLight)
```

---

## Testing

Run static analysis and type verification:

```bash
# Using Pyright
npx pyright
```

Quick endpoint verification with `curl`:

```bash
# Verify health
curl -s http://127.0.0.1:8000/v1/health

# Query live flight
curl -s http://127.0.0.1:8000/v1/flights/reg/EI-DEM

# Query aircraft around coordinates (e.g. Heathrow airport, 15 NM radius)
curl -s "http://127.0.0.1:8000/v1/flights/point/51.47/-0.45/15"
```

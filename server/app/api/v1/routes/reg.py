from fastapi import APIRouter, HTTPException, Depends

from app.domains.flights.schemas import FlightTelemetry
from app.domains.flights.client import ADSBClient, get_adsb_client

# Router initialization
router = APIRouter(tags=["registration"])


@router.get("/{registration}", response_model=FlightTelemetry)
async def get_aircraft_by_registration(registration: str, adsb_client: ADSBClient = Depends(get_adsb_client)) -> FlightTelemetry:
    """Fetch real-time flight telemetry for an aircraft by its registration (tail number).

    Args:
        registration: Aircraft registration / tail number (e.g., 'EI-DEM').
        adsb_client: Injected ADSBClient instance managing external API communication.

    Returns:
        FlightTelemetry: Standardized telemetry model containing position, speed, and altitude.

    Raises:
        HTTPException: 404 if the aircraft is not found or is currently offline.
        (Upstream 429, 502, and 504 errors are intercepted and handled by global exception handlers).
    """
    # 1. Fetch raw aircraft data from the upstream ADS-B domain client
    raw_plane = await adsb_client.get_by_registration(registration)
    if not raw_plane:
        raise HTTPException(
            status_code=404,
            detail=f"Aircraft with registration '{registration}' is not found or offline",
        )

    # 2. Map raw upstream ADS-B keys to the typed FlightTelemetry schema
    return FlightTelemetry(
        registration=raw_plane.get("r"),                  # Tail number (e.g., "EI-DEM")
        aircraft_type=raw_plane.get("t"),                 # ICAO aircraft type (e.g., "A320")
        latitude=raw_plane.get("lat"),                    # Latitude in decimal degrees
        longitude=raw_plane.get("lon"),                   # Longitude in decimal degrees
        altitude_barometric=raw_plane.get("alt_baro"),    # Barometric altitude in feet (or "ground")
        altitude_geometric=raw_plane.get("alt_geom"),     # GNSS/geometric altitude in feet
        ground_speed=raw_plane.get("gs"),                 # Ground speed in knots
        true_heading=raw_plane.get("true_heading"),       # Heading in degrees (0-360)
    )
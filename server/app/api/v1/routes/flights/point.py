from fastapi import APIRouter, Depends

from app.domains.flights.schemas import FlightTelemetryLight
from app.domains.flights.client import ADSBClient, get_adsb_client


# Router initialization
router = APIRouter()


@router.get("/{lat}/{lon}/{radius_nm}", response_model=list[FlightTelemetryLight])
async def get_aircrafts_by_point(
    lat: float,
    lon: float,
    radius_nm: float,
    adsb_client: ADSBClient = Depends(get_adsb_client),
) -> list[FlightTelemetryLight]:
    """Fetch real-time flight telemetry for all aircraft within a geographic radius of a point.

    Args:
        lat: Latitude of the center point in decimal degrees.
        lon: Longitude of the center point in decimal degrees.
        radius_nm: Search radius around the center point in nautical miles.
        adsb_client: Injected ADSBClient instance managing external API communication.

    Returns:
        list[FlightTelemetryLight]: List of standardized telemetry models for aircraft in range.

    Raises:
        HTTPException: 404 if no aircraft are found within the specified radius.
        (Upstream 429, 502, and 504 errors are intercepted and handled by global exception handlers).
    """
    # 1. Fetch raw aircraft data within geographic radius from the upstream ADS-B domain client
    raw_planes = await adsb_client.get_by_point(lat, lon, radius_nm)

    # 2. Map raw upstream ADS-B aircraft records to the typed FlightTelemetryLight schema
    return [
        FlightTelemetryLight(
            registration=p.get("r"),                  # Tail number (e.g., "EI-DEM")
            aircraft_type=p.get("t"),                 # ICAO aircraft type (e.g., "A320")
            latitude=p.get("lat"),                    # Latitude in decimal degrees
            longitude=p.get("lon"),                   # Longitude in decimal degrees
            true_heading=p.get("true_heading"),       # Heading in degrees (0-360)
        )
        for p in raw_planes
    ]
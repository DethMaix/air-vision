from pydantic import BaseModel, ConfigDict
from typing import Optional


class FlightTelemetry(BaseModel):
    """Schema representing real-time aircraft telemetry data."""

    # Aircraft identification
    registration: Optional[str] = None      # Tail number / registration (e.g., "EI-DEM")
    aircraft_type: Optional[str] = None     # ICAO aircraft type designator (e.g., "A320")
    
    # Position & navigation
    latitude: Optional[float] = None        # Latitude in decimal degrees
    longitude: Optional[float] = None       # Longitude in decimal degrees
    true_heading: Optional[float] = None    # Direction in degrees (0–360)
    
    # Altitude & speed
    altitude_barometric: Optional[int | str] = None  # Barometric altitude in feet (or "ground")
    altitude_geometric: Optional[int] = None         # GNSS/GPS altitude in feet
    ground_speed: Optional[float] = None             # Ground speed in knots

    # Allow instantiation from ORM models or arbitrary objects with attribute access
    model_config = ConfigDict(from_attributes=True)
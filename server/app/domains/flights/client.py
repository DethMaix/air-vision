import httpx

from collections.abc import AsyncGenerator
from json import JSONDecodeError
from typing import Optional

from app.domains.flights.exceptions import (
    ADSBTimeoutError,
    ADSBRateLimitError,
    ADSBUpstreamError,
)


class ADSBClient:
    """Asynchronous client for fetching aircraft data from the adsb.lol API."""

    def __init__(self, client: httpx.AsyncClient, timeout: float = 10.0) -> None:
        self.client = client
        self.base_url = "https://api.adsb.lol/"
        self.timeout = timeout
        # adsb.lol blocks generic HTTP client User-Agents and requires valid contact or project info
        self.headers = {
            "User-Agent": "AirVision/0.1.0 (github.com/DethMaix/air-vision)"
        }

    async def _get(self, endpoint: str) -> Optional[dict]:
        """Execute an HTTP GET request against an adsb.lol API endpoint.

        Handles network timeouts, rate limits, upstream server errors, and JSON decoding.

        Args:
            endpoint: Relative path of the API endpoint (e.g., 'v2/reg/EI-DEM').

        Returns:
            Optional[dict]: Parsed JSON response payload, or None if the resource is not found (404).

        Raises:
            ADSBTimeoutError: If the upstream request exceeds the configured timeout.
            ADSBRateLimitError: If the upstream API returns HTTP 429 Too Many Requests.
            ADSBUpstreamError: If the upstream API returns 5xx, unexpected status, connection error, or malformed JSON.
        """
        url = f"{self.base_url}{endpoint.lstrip('/')}"

        # 1. Execute request with network & timeout guards
        try:
            response = await self.client.get(url, headers=self.headers, timeout=self.timeout)
        except httpx.TimeoutException:
            raise ADSBTimeoutError("Upstream ADS-B service timed out. Please try again later.")
        except httpx.RequestError as e:
            raise ADSBUpstreamError(f"Unable to reach upstream ADS-B service: {e}")

        # 2. Resource not found (HTTP 404 indicates unknown registration or empty result)
        if response.status_code == 404:
            return None

        # 3. Rate limiting (HTTP 429 indicates client requests are being throttled)
        if response.status_code == 429:
            raise ADSBRateLimitError("Upstream ADS-B service is rate limiting requests. Please try again later.")

        # 4. Upstream server errors (HTTP 5xx)
        if response.status_code >= 500:
            raise ADSBUpstreamError(f"Upstream ADS-B service returned an unexpected server error ({response.status_code}).")

        # 5. Check for other unexpected 4xx client errors (e.g. 401 Unauthorized, 403 Forbidden)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ADSBUpstreamError(f"Upstream ADS-B service returned an unexpected error ({e.response.status_code}).")
        
        # 6. Parse JSON payload (httpx raises json.JSONDecodeError / ValueError on invalid JSON)
        try:
            data = response.json()
        except (JSONDecodeError, ValueError) as e:
            raise ADSBUpstreamError(f"Unable to decode JSON response from upstream ADS-B service: {e}")
        
        return data

    async def get_by_registration(self, registration: str) -> Optional[dict]:
        """Fetch raw telemetry data for an aircraft by registration (tail number).

        Args:
            registration: Tail number / registration string (e.g., 'EI-DEM').

        Returns:
            Optional[dict]: Raw telemetry dictionary if the aircraft is found and active,
                            or None if the aircraft is not found (404) or currently offline.

        Raises:
            ADSBTimeoutError: If the upstream service times out.
            ADSBRateLimitError: If upstream returns HTTP 429.
            ADSBUpstreamError: If upstream returns 5xx, connection fails, or response is invalid.
        """
        # Construct API endpoint for registration lookup (v2/reg/{registration})
        endpoint = f"v2/reg/{registration.upper()}"

        # Fetch aircraft data from upstream API
        data = await self._get(endpoint)
        if not data:
            return None

        # "ac" contains the list of active aircraft telemetry records
        planes = data.get("ac", []) 

        # Return None if the aircraft is currently offline / not sending data
        if not planes:
            return None

        return planes[0]

    async def get_by_point(self, lat: float, lon: float, radius_nm: float) -> list[dict]:
        """Fetch raw telemetry data for all aircraft within a geographic radius of a point.

        Args:
            lat: Latitude of the center point in decimal degrees.
            lon: Longitude of the center point in decimal degrees.
            radius_nm: Search radius around the center point in nautical miles.

        Returns:
            Optional[list[dict]]: List of raw aircraft telemetry dictionaries in the area,
                                  or None if no aircraft are detected or the area is empty.

        Raises:
            ADSBTimeoutError: If the upstream service times out.
            ADSBRateLimitError: If upstream returns HTTP 429.
            ADSBUpstreamError: If upstream returns 5xx, connection fails, or response is invalid.
        """
        # Construct API endpoint for geographic point radius query (v2/point/{lat}/{lon}/{radius_nm})
        endpoint = f"v2/point/{lat}/{lon}/{radius_nm}"

        # Fetch aircraft data from upstream API
        data = await self._get(endpoint)
        if not data:
            return []

        # "ac" contains the list of active aircraft telemetry records in the requested radius
        planes = data.get("ac", [])

        return planes


async def get_adsb_client() -> AsyncGenerator[ADSBClient, None]:
    """FastAPI dependency that yields an ADSBClient instance with a managed httpx session."""
    # 10s timeout to accommodate occasional latency spikes from the public API
    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        yield ADSBClient(client, timeout=10.0)


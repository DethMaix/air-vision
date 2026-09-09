# app/domains/flights/exceptions.py

class ADSBError(Exception):
    """Base exception for all ADS-B client errors."""
    pass


class ADSBTimeoutError(ADSBError):
    """Raised when the upstream service times out."""
    pass


class ADSBRateLimitError(ADSBError):
    """Raised when upstream returns HTTP 429."""
    pass


class ADSBUpstreamError(ADSBError):
    """Raised when upstream returns 5xx, invalid JSON, or connection fails."""
    pass
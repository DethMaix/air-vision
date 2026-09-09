from collections.abc import Callable
from typing import Any, cast
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domains.flights.exceptions import (
    ADSBTimeoutError,
    ADSBRateLimitError,
    ADSBUpstreamError,
)


# Handler for upstream network or gateway timeouts (HTTP 504)
async def adsb_timeout_error_handler(request: Request, e: ADSBTimeoutError) -> JSONResponse:
    """Handle ADS-B upstream timeouts by returning a 504 Gateway Timeout response."""
    return JSONResponse(
        status_code=504,
        content={"detail": str(e)},
    )


# Handler for upstream rate limiting / throttling (HTTP 429)
async def adsb_rate_limit_error_handler(request: Request, e: ADSBRateLimitError) -> JSONResponse:
    """Handle ADS-B upstream rate limits by returning a 429 Too Many Requests response."""
    return JSONResponse(
        status_code=429,
        content={"detail": str(e)},
    )


# Handler for upstream server failures, connection issues, or malformed responses (HTTP 502)
async def adsb_upstream_error_handler(request: Request, e: ADSBUpstreamError) -> JSONResponse:
    """Handle ADS-B upstream server/network errors by returning a 502 Bad Gateway response."""
    return JSONResponse(
        status_code=502,
        content={"detail": str(e)},
    )


# Centralized registration helper for attaching domain exception handlers to the FastAPI app
def register_exception_handlers(app: FastAPI) -> None:
    """Register custom domain exception handlers with the FastAPI application instance."""
    app.add_exception_handler(ADSBUpstreamError, cast(Callable[..., Any], adsb_upstream_error_handler))
    app.add_exception_handler(ADSBRateLimitError, cast(Callable[..., Any], adsb_rate_limit_error_handler))
    app.add_exception_handler(ADSBTimeoutError, cast(Callable[..., Any], adsb_timeout_error_handler))

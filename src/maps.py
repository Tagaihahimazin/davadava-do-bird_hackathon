"""Google Maps route utilities."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.request import urlopen


DIRECTIONS_ENDPOINT = "https://maps.googleapis.com/maps/api/directions/json"


class MapsError(RuntimeError):
    """Raised when Google Maps route lookup fails."""


@dataclass
class RouteSummary:
    origin: str
    destination: str
    distance_text: str
    distance_meters: int
    duration_text: str
    duration_seconds: int

    @property
    def duration_minutes(self) -> int:
        return max(1, round(self.duration_seconds / 60))



def get_drive_route_summary(origin: str, destination: str) -> RouteSummary:
    """Fetch driving route summary from Google Maps Directions API."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not api_key:
        raise MapsError("GOOGLE_MAPS_API_KEY is not set")

    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "departure_time": "now",
        "language": "ja",
        "key": api_key,
    }
    url = f"{DIRECTIONS_ENDPOINT}?{urlencode(params)}"

    try:
        with urlopen(url, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise MapsError(f"Failed to call Google Maps API: {exc}") from exc

    status = payload.get("status", "")
    if status != "OK":
        error_message = payload.get("error_message", "")
        details = f" ({error_message})" if error_message else ""
        raise MapsError(f"Google Maps API returned {status}{details}")

    routes = payload.get("routes", [])
    if not routes:
        raise MapsError("No routes returned")

    legs = routes[0].get("legs", [])
    if not legs:
        raise MapsError("No route legs returned")

    leg = legs[0]
    distance = leg.get("distance", {})
    duration = leg.get("duration_in_traffic") or leg.get("duration", {})

    return RouteSummary(
        origin=leg.get("start_address", origin),
        destination=leg.get("end_address", destination),
        distance_text=distance.get("text", "unknown"),
        distance_meters=int(distance.get("value", 0)),
        duration_text=duration.get("text", "unknown"),
        duration_seconds=int(duration.get("value", 0)),
    )

"""
eventlens Django middleware — auto-tracks page_view on every request.

Setup in settings.py::

    MIDDLEWARE = [
        ...
        "eventlens.django.eventlensMiddleware",
    ]

    eventlens_API_KEY = "ep_live_..."
    eventlens_ENDPOINT = "https://eventlens-analytics-backend.onrender.com"  # optional
"""
from __future__ import annotations

from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from eventlens.client import eventlensClient

_client: eventlensClient | None = None


def _get_client() -> eventlensClient:
    global _client
    if _client is None:
        _client = eventlensClient(
            api_key=settings.eventlens_API_KEY,
            endpoint=getattr(settings, "eventlens_ENDPOINT", "https://eventlens-analytics-backend.onrender.com"),
        )
    return _client


class eventlensMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        _get_client()   # eager init

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        client = _get_client()
        user_id = str(request.user.pk) if getattr(request, "user", None) and request.user.is_authenticated else None
        if user_id:
            client._user_id = user_id

        client.track("page_view", {
            "url": request.build_absolute_uri(),
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "referrer": request.META.get("HTTP_REFERER"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        })

        return response
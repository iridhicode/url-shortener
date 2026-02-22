"""Pydantic request and response schemas for the URL shortener API."""

from pydantic import BaseModel, HttpUrl


class URLRequest(BaseModel):
    """Request body for the URL shortening endpoint."""

    url: HttpUrl


class ShortenResponse(BaseModel):
    """Response body returned after successfully shortening a URL."""

    short_url: str
    status: str

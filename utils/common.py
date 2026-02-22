"""Common utility functions for the URL shortener."""

import secrets
import string

from constants import SHORT_ID_LENGTH


def generate_shorten_url(length: int = SHORT_ID_LENGTH) -> str:
    """Generate a cryptographically secure random short ID."""
    characters: str = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

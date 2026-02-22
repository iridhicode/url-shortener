"""Database helper functions for URL CRUD operations."""

import logging
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models.models as models
from constants import MAX_COLLISION_RETRIES
from utils.common import generate_shorten_url

logger = logging.getLogger(__name__)


def get_url_by_short_id(db: Session, short_id: str) -> Optional[models.URLs]:
    """Return the URL record matching the given short ID, or None."""
    return db.query(models.URLs).filter(models.URLs.short_id == short_id).first()


def create_url(db: Session, long_url: str) -> models.URLs:
    """Create a new shortened URL, retrying on short-ID collisions.

    Raises RuntimeError if a unique short ID cannot be generated after
    MAX_COLLISION_RETRIES attempts.
    """
    for attempt in range(MAX_COLLISION_RETRIES):
        short_id = generate_shorten_url()
        db_url = models.URLs(short_id=short_id, long_url=long_url)
        try:
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
        except IntegrityError:
            db.rollback()
            logger.warning(
                "Short-ID collision on attempt %d for id=%s", attempt + 1, short_id
            )
    raise RuntimeError("Failed to generate a unique short ID after retries")

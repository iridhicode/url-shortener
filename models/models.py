"""SQLAlchemy ORM models for the URL shortener."""

from sqlalchemy import Column, DateTime, Integer, String, func

from db.database import Base


class URLs(Base):
    """Stores the mapping between short IDs and their original long URLs."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String, unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

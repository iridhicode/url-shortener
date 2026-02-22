"""Database engine and session configuration."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from constants import DEFAULT_DATABASE_URL

SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

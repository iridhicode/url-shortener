"""FastAPI application for the URL shortener service."""

import logging
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import models.models as models
from db.database import SessionLocal, engine
from models.request import ShortenResponse, URLRequest
from utils.db import create_url, get_url_by_short_id

logger = logging.getLogger(__name__)

app = FastAPI(
    title="URL Shortener",
    description="URL Shortener API using FastAPI and SQLite",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """Return a simple health-check response."""
    return {"status": "ok"}


@app.post("/shorten", tags=["URL Shortener"], response_model=ShortenResponse)
def shorten_url_func(
    url_request: URLRequest, db: Session = Depends(get_db)
) -> ShortenResponse:
    """Shorten a URL and return the generated short ID."""
    try:
        long_url = str(url_request.url)
        db_url = create_url(db, long_url)
        return ShortenResponse(short_url=db_url.short_id, status="success")
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error occurred while shortening URL: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error while trying to shorten the URL",
        )


@app.get("/{short_id}", tags=["URL Shortener"])
def redirect_url(short_id: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """Redirect the caller to the original long URL for the given short ID."""
    try:
        db_url = get_url_by_short_id(db, short_id)
        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")
        long_url = db_url.long_url
        if not long_url.startswith("http"):
            long_url = "https://" + long_url
        return RedirectResponse(url=long_url)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error occurred while redirecting URL: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error while calling the redirect URL",
        )

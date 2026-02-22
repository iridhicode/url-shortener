"""Tests for the URL shortener API endpoints."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from db.database import Base
from main import app, get_db


@pytest.fixture()
def client():
    """Return a TestClient wired to a shared in-memory test database."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def _override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_endpoint(client: TestClient) -> None:
    """Verify the health endpoint returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_url_success(client: TestClient) -> None:
    """Verify a valid URL is shortened successfully."""
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["short_url"]) == 8


def test_shorten_url_invalid_url(client: TestClient) -> None:
    """Verify that an invalid URL is rejected with a 422 error."""
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422


def test_redirect_existing_short_id(client: TestClient) -> None:
    """Verify redirect to the original URL for a known short ID."""
    shorten_resp = client.post(
        "/shorten", json={"url": "https://example.com/test"}
    )
    short_id = shorten_resp.json()["short_url"]
    response = client.get(f"/{short_id}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/test"


def test_redirect_unknown_short_id(client: TestClient) -> None:
    """Verify that an unknown short ID returns a 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"


@patch(
    "utils.db.generate_shorten_url",
    side_effect=["AAAAAAAA", "AAAAAAAA", "BBBBBBBB"],
)
def test_shorten_url_collision_retry(mock_gen, client: TestClient) -> None:
    """Verify that a short-ID collision is retried and succeeds."""
    resp1 = client.post("/shorten", json={"url": "https://example.com/one"})
    assert resp1.status_code == 200
    assert resp1.json()["short_url"] == "AAAAAAAA"

    resp2 = client.post("/shorten", json={"url": "https://example.com/two"})
    assert resp2.status_code == 200
    assert resp2.json()["short_url"] == "BBBBBBBB"


@pytest.mark.parametrize(
    "url",
    [
        pytest.param("javascript:alert(1)", id="javascript-uri"),
        pytest.param("data:text/html,<h1>hi</h1>", id="data-uri"),
        pytest.param("file:///etc/passwd", id="file-uri"),
        pytest.param("", id="empty-string"),
    ],
)
def test_shorten_url_rejects_dangerous_urls(
    client: TestClient, url: str
) -> None:
    """Verify that non-http/https URLs are rejected."""
    response = client.post("/shorten", json={"url": url})
    assert response.status_code == 422

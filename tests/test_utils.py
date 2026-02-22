"""Tests for utility functions."""

import pytest

from utils.common import generate_shorten_url


def test_generate_shorten_url_default_length() -> None:
    """Verify the default generated short ID has 8 characters."""
    result = generate_shorten_url()
    assert len(result) == 8


@pytest.mark.parametrize(
    "length",
    [
        pytest.param(4, id="short-4"),
        pytest.param(12, id="long-12"),
        pytest.param(16, id="long-16"),
    ],
)
def test_generate_shorten_url_custom_length(length: int) -> None:
    """Verify the generated short ID matches the requested length."""
    result = generate_shorten_url(length=length)
    assert len(result) == length


def test_generate_shorten_url_alphanumeric() -> None:
    """Verify the generated short ID contains only alphanumeric characters."""
    result = generate_shorten_url()
    assert result.isalnum()


def test_generate_shorten_url_uniqueness() -> None:
    """Verify that consecutive generated IDs are very likely to differ."""
    ids = {generate_shorten_url() for _ in range(100)}
    assert len(ids) == 100

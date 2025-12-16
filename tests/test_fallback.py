
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@patch("app.main.address_fetcher")
def test_generate_address_unknown_country_fallback(mock_address_fetcher):
    """
    Test that when an unknown country is provided, the API defaults to US
    instead of raising a 400 error.
    """
    # Setup mock return value for success case
    mock_address_fetcher.fetch_real_address.return_value = {
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "zipcode": "12345",
        "country": "United States",
        "full_address": "123 Test St, Test City, TS, United States"
    }

    response = client.get("/api/generate?country=UnknownLand")

    assert response.status_code == 200

    # Verify fetch_real_address was called with "US"
    # normalize("UnknownLand") returns None, so main.py should set country_code="US"
    args, _ = mock_address_fetcher.fetch_real_address.call_args
    assert args[0] == "US"

    data = response.json()
    assert data["country"] == "United States"

@patch("app.main.address_fetcher")
def test_generate_address_known_country(mock_address_fetcher):
    """
    Test that when a known country is provided, the API uses it.
    """
    mock_address_fetcher.fetch_real_address.return_value = {
        "address": "10 Downing St",
        "city": "London",
        "state": "London",
        "zipcode": "SW1A 2AA",
        "country": "United Kingdom",
        "full_address": "10 Downing St, London, United Kingdom"
    }

    response = client.get("/api/generate?country=UK")

    assert response.status_code == 200

    # Verify fetch_real_address was called with "GB" (normalized UK)
    args, _ = mock_address_fetcher.fetch_real_address.call_args
    assert args[0] == "GB"

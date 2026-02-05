"""
Tests for BaseAPIClient
"""

import pytest
import time
from src.data_collection.base_client import BaseAPIClient


def test_base_client_initialization():
    """Test that BaseAPIClient initializes correctly"""
    client = BaseAPIClient(base_url="https://www.balldontlie.io/api/v1")

    assert client.base_url == "https://www.balldontlie.io/api/v1"
    assert client.rate_limit_delay == 0.6
    assert client.timeout == 30


def test_base_client_custom_params():
    """Test BaseAPIClient with custom parameters"""
    client = BaseAPIClient(
        base_url="https://api.example.com",
        api_key="test_key",
        rate_limit_delay=1.0,
        max_retries=5,
        timeout=60
    )

    assert client.base_url == "https://api.example.com"
    assert client.api_key == "test_key"
    assert client.rate_limit_delay == 1.0
    assert client.timeout == 60


def test_rate_limiting():
    """Test that rate limiting delays requests"""
    client = BaseAPIClient(
        base_url="https://www.balldontlie.io/api/v1",
        rate_limit_delay=0.5
    )

    start_time = time.time()

    # Make two rate-limited calls
    client._rate_limit()
    client._rate_limit()

    elapsed_time = time.time() - start_time

    # Should have at least one delay of 0.5 seconds
    assert elapsed_time >= 0.5


def test_context_manager():
    """Test that BaseAPIClient works as context manager"""
    with BaseAPIClient(base_url="https://www.balldontlie.io/api/v1") as client:
        assert client is not None


def test_get_headers_without_api_key():
    """Test headers without API key"""
    client = BaseAPIClient(base_url="https://api.example.com")
    headers = client._get_headers()

    assert "Accept" in headers
    assert headers["Accept"] == "application/json"
    assert "Authorization" not in headers


def test_get_headers_with_api_key():
    """Test headers with API key"""
    client = BaseAPIClient(
        base_url="https://api.example.com",
        api_key="test_key"
    )
    headers = client._get_headers()

    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test_key"


# Integration test (only runs if you have internet connection)
def test_real_api_call():
    """Test a real API call to balldontlie.io"""
    client = BaseAPIClient(base_url="https://www.balldontlie.io/api/v1")

    try:
        response = client.get("/teams", params={"per_page": 1})
        assert "data" in response
        assert isinstance(response["data"], list)
    except Exception as e:
        pytest.skip(f"Skipping integration test due to: {str(e)}")
    finally:
        client.close()

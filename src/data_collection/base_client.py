"""
Base API Client for NBA Data Collection

This module provides a base class for making API requests with:
- Rate limiting
- Retry logic
- Error handling
- Logging

Usage:
    from src.data_collection.base_client import BaseAPIClient

    client = BaseAPIClient(base_url="https://api.example.com")
    data = client.get("/endpoint")
"""

import time
import requests
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseAPIClient:
    """Base class for API clients with built-in retry and rate limiting"""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        rate_limit_delay: float = 0.6,  # seconds between requests
        max_retries: int = 3,
        timeout: int = 30
    ):
        """
        Initialize the API client

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
            rate_limit_delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        self.last_request_time = 0

        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {
            "Accept": "application/json",
            "User-Agent": "NBA-Performance-Prediction/0.1.0"
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return headers

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API

        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Optional query parameters

        Returns:
            JSON response as dictionary

        Raises:
            requests.exceptions.HTTPError: If request fails
        """
        self._rate_limit()

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage
if __name__ == "__main__":
    # Example: Using balldontlie.io API
    client = BaseAPIClient(base_url="https://www.balldontlie.io/api/v1")

    try:
        # Fetch some teams
        teams = client.get("/teams")
        print(f"Fetched {len(teams.get('data', []))} teams")

    finally:
        client.close()

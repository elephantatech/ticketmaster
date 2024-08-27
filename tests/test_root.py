"""
TicketMaster Application - Root Endpoint Test.

This module contains a unit test for the root endpoint of the TicketMaster application's API.
The root endpoint typically provides a welcome message or basic information about the API.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI instance
from app.main import settings

client = TestClient(app)


def test_root_endpoint():
    """
    Test the root endpoint to ensure it responds with the expected welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_startup_event():
    """
    Test the startup_event function.

    This test checks that aioredis.from_url and logger.info are called with the correct arguments when startup_event is called, 
    and that app.state.redis is set correctly.
    """
    # Mock aioredis.from_url and logger.info
    with patch('aioredis.from_url') as mock_redis, patch('app.main.logger.info') as mock_logger:
        # Set up the mock objects
        mock_redis.return_value = MagicMock()
        mock_logger.return_value = None

        # Call the startup_event function
        await app.on_event("startup")()

        # Assert that aioredis.from_url was called with the correct arguments
        mock_redis.assert_called_once_with(settings.REDIS_URL, decode_responses=True)

        # Assert that logger.info was called with the correct arguments
        mock_logger.assert_called_once_with("Startup event triggered. Redis connection established.")

        # Assert that app.state.redis was set correctly
        assert isinstance(app.state.redis, MagicMock)


if __name__ == "__main__":
    test_root_endpoint()  # For quick standalone testing purposes. Remove if unnecessary.

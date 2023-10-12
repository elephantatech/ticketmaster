"""
TicketMaster Application - Root Endpoint Test.

This module contains a unit test for the root endpoint of the TicketMaster application's API.
The root endpoint typically provides a welcome message or basic information about the API.
"""

from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI instance

client = TestClient(app)


def test_root_endpoint():
    """
    Test the root endpoint to ensure it responds with the expected welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


if __name__ == "__main__":
    test_root_endpoint()  # For quick standalone testing purposes. Remove if unnecessary.

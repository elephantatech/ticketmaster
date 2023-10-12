"""
TicketMaster Application - Test Module.

This module contains unit tests for the TicketMaster application's API endpoints.
Each test is designed to simulate API endpoint behavior and ensure correct operation.

Test Cases Covered:
1. Creating a new ticket.
2. Retrieving a ticket by its unique identifier.
3. Updating a ticket's attributes.
4. Deleting a ticket by its unique identifier.
5. Retrieving all available tickets.

All database operations are mocked using the MockRedis class to avoid any actual
database operations, ensuring tests run in isolation without side effects.

Each test uses FastAPI's `TestClient` for sending HTTP requests and validating the
responses.

Note:
Ensure the application's environment is set up for testing before running these tests.
For best practices, run these tests in an isolated environment (like a CI/CD pipeline or a
dedicated test environment).

"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class MockRedis:
    """
    A mock Redis class that simulates basic Redis operations in memory.
    Useful for testing purposes without affecting an actual database.
    """

    def __init__(self):
        """Initialize an empty store to simulate Redis in-memory storage."""
        self.store = {}

    async def hset(self, key, field=None, value=None, mapping=None):
        """Simulate the HSET operation of Redis."""
        if key not in self.store:
            self.store[key] = {}
        if mapping:
            self.store[key].update(mapping)
        else:
            self.store[key][field] = value
        return True

    async def hgetall(self, key):
        """Simulate the hgetall operation of Redis."""
        return self.store.get(key, {})

    async def hget(self, key, field):
        """Simulate the hget operation of Redis."""
        return self.store.get(key, {}).get(field)

    async def delete(self, key):
        """Simulate the delete operation of Redis."""
        if key in self.store:
            del self.store[key]
        return True

    async def exists(self, key):
        """Simulate the exists operation of Redis."""
        return key in self.store

    async def keys(self, _pattern):
        """Simulate the keys operation of Redis."""
        return list(self.store.keys())

    async def expire(self, key, ttl):
        """Simulate the expire operation of Redis.
        Note: This mock implementation does not actually do anything related to expiration.
        """


def test_create_ticket(monkeypatch):
    """
    Test the endpoint for creating a new ticket.
    Validates the successful creation and correct response structure.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)

    response = client.post(
        "/tickets/", json={"id": "123455", "title": "Test Ticket", "status": "Open"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["status"] == "Open"


def test_get_ticket(monkeypatch):
    """
    Test the endpoint to retrieve a ticket using its unique ID.
    Validates the correct retrieval and response structure.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)

    # Create a ticket
    client.post(
        "/tickets/", json={"id": "123455", "title": "Test Ticket", "status": "Open"}
    )

    ticket_id = list(mock_redis.store.keys())[0]
    response = client.get(f"/tickets/{ticket_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["status"] == "Open"


def test_get_ticket_not_found(monkeypatch):
    """
    Test the endpoint to retrieve a ticket using its unique ID.
    Validates if not valid ticket with id exists in the redis store.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)
    response = client.get("/tickets/123456/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_update_ticket(monkeypatch):
    """
    Test the endpoint to update the attributes of a ticket using its unique ID.
    Validates the successful update and correct response structure.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)

    # Create a ticket
    client.post(
        "/tickets/", json={"id": "123455", "title": "Test Ticket", "status": "Open"}
    )

    ticket_id = list(mock_redis.store.keys())[0]
    updatedata = {"status": "Updated", "title": "Test Ticket Updated", "details": ""}
    response = client.put(f"/tickets/{ticket_id}/", json=updatedata)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Ticket Updated"
    assert data["status"] == "Updated"


def test_update_ticket_not_found(monkeypatch):
    """
    Test the endpoint to update the attributes of a ticket using its unique ID.
    Validates if the ticket is not found if the ticket is not in the redis store.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)
    updatedata = {"status": "Updated", "title": "Test Ticket Updated", "details": ""}
    response = client.put("/tickets/12345/", json=updatedata)
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_delete_ticket(monkeypatch):
    """
    Test the endpoint to delete a ticket using its unique ID.
    Validates the successful deletion.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)

    # Create a ticket
    client.post(
        "/tickets/", json={"id": "123455", "title": "Test Ticket", "status": "Open"}
    )

    ticket_id = list(mock_redis.store.keys())[0]

    response = client.delete(f"/tickets/{ticket_id}/")
    assert response.status_code == 200


def test_delete_ticket_not_found(monkeypatch):
    """
    Test the endpoint to delete a ticket using its unique ID.
    Validates the successful deletion.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)
    response = client.delete("/tickets/123455")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


def test_get_all_ticket(monkeypatch):
    """
    Test the endpoint to retrieve all the tickets.
    Validates the correct retrieval and response structure.
    """
    mock_redis = MockRedis()
    app.state.redis = mock_redis
    monkeypatch.setattr(app.state, "redis", mock_redis)

    # Create a ticket
    client.post(
        "/tickets/", json={"id": "123455", "title": "Test Ticket", "status": "Open"}
    )
    client.post(
        "/tickets/", json={"id": "123456", "title": "Test Ticket 2", "status": "Open"}
    )

    response = client.get("/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 2

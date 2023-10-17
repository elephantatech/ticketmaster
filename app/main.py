"""
TicketMaster Application - Main module.

This module sets up the FastAPI application and defines all its routes.
It also handles startup and shutdown events for the app, such as
connecting to and closing the Redis database connection.

Routes:
1. root (`/`) - Returns a simple hello world message.
2. create_ticket (`/tickets/`) - Allows the creation of a new ticket.
3. update_ticket (`/tickets/{ticket_id}/`) - Allows updating an existing ticket by ID.
4. get_ticket (`/tickets/{ticket_id}/`) - Retrieves the details of a ticket by ID.
5. get_all_tickets (`/tickets/`) - Lists all existing tickets.
6. delete_ticket (`/tickets/{ticket_id}/`) - Deletes a ticket by ID.

Additionally, the module configures logging for the application and can
be run directly to launch the app using Uvicorn.
"""

import os
import logging.config
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
import uvicorn

from redis import asyncio as aioredis


from app.model import Ticket, TicketCreate, TicketUpdate, TicketUpdateRequest
from app.config import settings

LOGGING_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "logging.ini"
)
logging.config.fileConfig(LOGGING_CONFIG_PATH, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Startup event function. Establishes a connection to Redis."""
    app.state.redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    logger.info("Startup event triggered. Redis connection established.")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event function. Closes the connection to Redis."""
    await app.state.redis.close()
    logger.info("Shutdown event triggered. Redis connection closed.")


@app.get("/")
async def root():
    """Root endpoint. Returns a Hello World message."""
    logger.info("Root endpoint was called")
    return {"message": "Hello World"}


@app.post("/tickets/", response_model=Ticket)
async def create_ticket(ticket: TicketCreate) -> Ticket:
    """
    Endpoint to create a new ticket.

    Args:
        ticket (TicketCreate): Ticket data.

    Returns:
        Ticket: Created ticket data.
    """
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    ticket_data = Ticket(
        id=ticket.id,
        title=ticket.title,
        status=ticket.status,
        details=ticket.details if ticket.details else "",
        created_date=now_str,
        updated_date=now_str,
    )

    # Save to Redis
    await app.state.redis.hset(ticket_data.id, mapping=ticket_data.model_dump())

    # Compute expiration time (2 weeks from created_date)
    expiration_time = now + timedelta(weeks=2)
    # Calculate time difference in seconds
    ttl = int((expiration_time - now).total_seconds())

    # Set the expiration time for the hash
    await app.state.redis.expire(ticket_data.id, ttl)

    created_ticket = await app.state.redis.hgetall(ticket_data.id)
    logger.info(
        "Created a new ticket with ID: %s",
        ticket_data.id,
        extra={"ticket": created_ticket},
    )

    return Ticket(**created_ticket)


@app.put("/tickets/{ticket_id}/", response_model=Ticket)
async def update_ticket(ticket_id: str, ticket: TicketUpdateRequest) -> Ticket:
    """
    Endpoint to update an existing ticket.

    Args:
        ticket_id (str): Ticket ID.
        ticket (TicketUpdateRequest): Updated ticket data.

    Returns:
        Ticket: Updated ticket data.
    """
    if not await app.state.redis.exists(ticket_id):
        raise HTTPException(status_code=404, detail="Ticket not found")
    update_data = TicketUpdate(
        **ticket.model_dump(), updated_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    ticket_data = await app.state.redis.hgetall(ticket_id)
    await app.state.redis.hset(ticket_id, mapping=update_data.model_dump())

    updated_ticket = await app.state.redis.hgetall(ticket_id)
    logger.info(
        "Updated ticket with ID: %s",
        id,
        extra={"original": ticket_data, "Updated": updated_ticket},
    )

    return Ticket(**updated_ticket)


@app.get("/tickets/{ticket_id}/", response_model=Ticket)
async def get_ticket(ticket_id: str) -> Ticket:
    """
    Endpoint to retrieve a ticket by its ID.

    Args:
        ticket_id (str): Ticket ID.

    Returns:
        Ticket: Requested ticket data.
    """
    ticket_data = await app.state.redis.hgetall(ticket_id)
    if not ticket_data:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return Ticket(**ticket_data)


@app.get("/tickets/", response_model=list[Ticket])
async def get_all_tickets() -> list[Ticket]:
    """
    Endpoint to retrieve all tickets.

    Returns:
        list[Ticket]: List of all tickets.
    """
    keys = await app.state.redis.keys("*")
    tickets = []
    for key in keys:
        ticket_data = await app.state.redis.hgetall(key)
        if ticket_data:
            tickets.append(Ticket(**ticket_data))
    return tickets


@app.delete("/tickets/{ticket_id}/")
async def delete_ticket(ticket_id: str) -> dict:
    """
    Endpoint to delete a ticket by its ID.

    Args:
        ticket_id (str): Ticket ID.

    Returns:
        dict: Status of the deletion.
    """
    if not await app.state.redis.exists(ticket_id):
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket_data = await app.state.redis.hgetall(ticket_id)
    await app.state.redis.delete(ticket_id)
    logger.info("Deleted ticket with ID: %s", id, extra={"ticket": ticket_data})
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        log_config="logging.ini",
        reload=True,
    )

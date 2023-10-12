"""
Models for the TicketMaster application.

This module defines the Pydantic models used for request and response payloads
in the TicketMaster application. These models include:

1. TicketCreate - Data model for creating a new ticket.
2. TicketUpdateRequest - Data model for the request to update an existing ticket.
3. TicketUpdate - Data model for updating an existing ticket with an updated date.
4. Ticket - Data model for representing a ticket in response payloads.
"""

from typing import Optional
from pydantic import BaseModel


# Request Models
class TicketCreate(BaseModel):
    """
    Data model for creating a new ticket.

    Attributes:
        title (str): The title of the ticket.
        status (str): The current status of the ticket.
        details (Optional[str]): Additional details about the ticket. Defaults to None.
        id (str, optional): The unique identifier for the ticket. Defaults to None.
    """

    title: str
    status: str
    details: Optional[str] = ""
    id: str = ""


class TicketUpdateRequest(BaseModel):
    """
    Data model for the request to update an existing ticket.

    Attributes:
        title (str, optional): The updated title of the ticket. Defaults to None.
        status (str, optional): The updated status of the ticket. Defaults to None.
        details (str, optional): Updated details about the ticket. Defaults to None.
    """

    title: str = ""
    status: str = ""
    details: str = ""


class TicketUpdate(BaseModel):
    """
    Data model for updating an existing ticket with an updated date.

    Attributes:
        title (str, optional): The updated title of the ticket. Defaults to None.
        status (str, optional): The updated status of the ticket. Defaults to None.
        details (str, optional): Updated details about the ticket. Defaults to None.
        updated_date (str): The date when the ticket was last updated.
    """

    title: str = ""
    status: str = ""
    details: str = ""
    updated_date: str


# Response Models
class Ticket(BaseModel):
    """
    Data model for representing a ticket in response payloads.

    Attributes:
        id (str): The unique identifier for the ticket.
        title (str): The title of the ticket.
        status (str): The current status of the ticket.
        details (str): Additional details about the ticket.
        created_date (str): The date when the ticket was created.
        updated_date (str): The date when the ticket was last updated.
    """

    id: str
    title: str
    status: str
    details: str
    created_date: str
    updated_date: str

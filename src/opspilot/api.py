
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from opspilot.models import Ticket
from opspilot.manager import TicketManager
from opspilot.database import initialize_database
from opspilot.classifier import classify_ticket


app = FastAPI(
    title="OpsPilot API",
    description="IT Support Ticket Management System",
    version="1.0.0"
)

initialize_database()

manager = TicketManager()


class TicketCreate(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


# 1. Insert ticket
@app.post("/tickets")
def create_ticket(data: TicketCreate):

    result = classify_ticket(data.description)

    try:
        ticket = Ticket(
            id=data.id,
            title=data.title,
            description=data.description,
            category=result["category"],
            priority=result["priority"]
        )

        return manager.add_ticket(ticket)

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ticket ID already exists"
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# 2. Get all tickets
@app.get("/tickets")
def get_tickets():

    return manager.get_all_tickets()


# 3. Search ticket by ID
@app.get("/tickets/{ticket_id}")
def search_ticket(ticket_id: str):

    ticket = manager.search_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket

class TicketStatusUpdate(BaseModel):
    status: str

@app.patch("/tickets/{ticket_id}/status")
def update_status(ticket_id: str, data: TicketStatusUpdate):

    status = data.status.strip().upper()

    if status not in Ticket.VALID_STATUS:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status"
        )

    updated = manager.update_ticket_status(ticket_id, status)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return manager.search_ticket(ticket_id)
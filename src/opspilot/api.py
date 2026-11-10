from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3

from opspilot.models import Ticket
from opspilot.manager import TicketManager
from opspilot.database import initialize_database
from opspilot.classifier import classify_ticket
from opspilot.ai_helper import analyze_ticket_with_ai

app = FastAPI(
    title="OpsPilot API",
    description="IT Support Ticket Management System with Gemini AI",
    version="1.0.0"
)

initialize_database()
manager = TicketManager()

class TicketCreate(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)

class StatusUpdate(BaseModel):
    status: str

@app.get("/tickets")
def get_tickets():
    """Retrieve all support tickets."""
    return manager.get_all_tickets()

@app.post("/tickets")
def create_ticket(data: TicketCreate):
    """Create a new support ticket enriched with rule-based and Gemini AI insights."""
    rule_result = classify_ticket(data.description)
    ai_result = analyze_ticket_with_ai(data.description)

    try:
        ticket = Ticket(
            id=data.id,
            title=data.title,
            description=data.description,
            category=rule_result.get("category", "SOFTWARE"),
            priority=rule_result.get("priority", "MEDIUM")
        )

        saved_ticket = manager.add_ticket(ticket)

        return {
            **saved_ticket,
            "ai_insights": ai_result.get("ai_analysis", "No AI analysis available")
        }

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Ticket ID already exists")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.patch("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: str, payload: StatusUpdate):
    """Update the status of an existing ticket."""
    updated = manager.update_ticket_status(ticket_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated

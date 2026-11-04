
import sqlite3
from contextlib import contextmanager

DB_NAME = "opspilot.db"


# Create and safely manage database connections
@contextmanager
def get_connection():

    connection = sqlite3.connect(
        DB_NAME,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    try:
        yield connection

    finally:
        connection.close()


# Initialize database
def initialize_database():

    with get_connection() as connection:

        connection.execute("""
            PRAGMA journal_mode=WAL
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                sla_deadline TEXT NOT NULL,
                escalated INTEGER NOT NULL
            )
        """)

        connection.commit()


# Insert a ticket
def save_ticket(ticket):

    with get_connection() as connection:

        connection.execute("""
            INSERT INTO tickets
            (id, title, description, category, priority,
             status, created_at, sla_deadline, escalated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket.id,
            ticket.title,
            ticket.description,
            ticket.category,
            ticket.priority,
            ticket.status,
            ticket.created_at.isoformat(),
            ticket.sla_deadline.isoformat(),
            int(ticket.escalated)
        ))

        connection.commit()


# Get all tickets
def get_all_tickets():

    with get_connection() as connection:

        rows = connection.execute(
            "SELECT * FROM tickets"
        ).fetchall()

        return [dict(row) for row in rows]


# Get a specific ticket
def get_ticket_by_id(ticket_id):

    with get_connection() as connection:

        row = connection.execute(
            "SELECT * FROM tickets WHERE id = ?",
            (ticket_id.upper(),)
        ).fetchone()

        return dict(row) if row else None


# Update ticket status
def update_ticket_status(ticket_id, status):

    with get_connection() as connection:

        cursor = connection.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (status.upper(), ticket_id.upper())
        )

        connection.commit()

        return cursor.rowcount > 0

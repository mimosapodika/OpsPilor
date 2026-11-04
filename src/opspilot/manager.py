
from opspilot.database import (
    save_ticket,
    get_all_tickets,
    get_ticket_by_id,
)


class TicketManager:

    def add_ticket(self, ticket):
        save_ticket(ticket)
        return get_ticket_by_id(ticket.id)

    def get_all_tickets(self):
        return get_all_tickets()

    def search_ticket(self, ticket_id):
        return get_ticket_by_id(ticket_id)

    def update_ticket_status(self, ticket_id, status):
        from opspilot.database import update_ticket_status
        return update_ticket_status(ticket_id, status)
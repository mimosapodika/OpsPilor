
from datetime import datetime, timedelta


class Ticket:

    VALID_CATEGORIES = {
        "HARDWARE",
        "NETWORK",
        "SECURITY",
        "SOFTWARE"
    }

    VALID_PRIORITY = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    }

    VALID_STATUS = {
        "OPEN",
        "PENDING",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    }

    SLA_HOURS = {
        "CRITICAL": 1,
        "HIGH": 4,
        "MEDIUM": 12,
        "LOW": 24
    }

    def __init__(
        self,
        id,
        title,
        description,
        category,
        priority,
        status="OPEN"
    ):

        self.id = id.strip().upper()
        self.title = title.strip()
        self.description = description.strip()

        self.category = category.strip().upper()
        self.priority = priority.strip().upper()
        self.status = status.strip().upper()

        # Basic validation
        if not self.id:
            raise ValueError("Ticket ID cannot be empty")

        if not self.title:
            raise ValueError("Ticket title cannot be empty")

        if not self.description:
            raise ValueError("Ticket description cannot be empty")

        if self.category not in self.VALID_CATEGORIES:
            raise ValueError("Invalid ticket category")

        if self.priority not in self.VALID_PRIORITY:
            raise ValueError("Invalid ticket priority")

        if self.status not in self.VALID_STATUS:
            raise ValueError("Invalid ticket status")

        # Ticket creation time
        self.created_at = datetime.now()

        # SLA deadline based on priority
        self.sla_deadline = (
            self.created_at
            + timedelta(hours=self.SLA_HOURS[self.priority])
        )

        self.escalated = False

    def display(self):

        print("\n----- TICKET DETAILS -----")
        print("ID:", self.id)
        print("Title:", self.title)
        print("Description:", self.description)
        print("Category:", self.category)
        print("Priority:", self.priority)
        print("Status:", self.status)
        print("Created At:", self.created_at)
        print("SLA Deadline:", self.sla_deadline)
        print("Escalated:", self.escalated)
        print("--------------------------")

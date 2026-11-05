🎫 OpsPilot — IT Support Ticket Management System

OpsPilot is a lightweight IT Support Ticket Management System that automatically classifies, prioritizes, and tracks IT support requests via a FastAPI backend and a Streamlit dashboard.

🚀 Features

- **Automated Triage**: Python rule-based engine classifies tickets (Hardware, Network, Security, Software) and sets priorities (Critical to Low).
- **Queue Sorting Automatically** pushes critical and high-priority tickets to the top of the queue.
- **Interactive Dashboard** Live tracking of metrics (total, open, critical tickets) and status management for admins.
- **REST API & Search:** Full CRUD capability for ticket lifecycles and unique ID lookups.
- **Persistent Storage:** Local, self-initializing SQLite database.

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn, Requests
- **Frontend:** Streamlit
- **Database:** SQLite
- **Environment Management:** `uv`

## 🏗️ System Architecture & Structure

```text
       User ──> Streamlit Dashboard ──> FastAPI Backend ──> [ Rule Classifier | SQLite DB ]
```

```text
OpsPilot/
├── .streamlit/secrets.toml    # Credentials
├── src/opspilot/              # Core source (api, classifier, database, models)
├── dashboard.py               # Streamlit interface
├── pyproject.toml & uv.lock   # Project dependencies
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone & Install
Ensure [uv](https://docs.astral.sh/uv/) is installed.
```bash
git clone https://github.com/mimosapodika/OpsPilor.git
cd OpsPilor
uv sync
```

### 2. Configure Credentials
Create `.streamlit/secrets.toml` in the root directory (do not commit to GitHub):
```toml
[admin]
username = "admin"
password = "YOUR_PRIVATE_PASSWORD"
```

### 3. Start Services
Run the **FastAPI Backend**:
```bash
uv run uvicorn opspilot.api:app --reload
```
*Docs available at:* `http://127.0.0.1:8000/docs`

Run the **Streamlit Dashboard** in a second terminal:
```bash
# Windows PowerShell env setup
\$env:STREAMLIT_CONFIG_DIR = (Join-Path (Get-Location).Path ".streamlit")

uv run streamlit run dashboard.py --server.headless true --browser.gatherUsageStats false
```
*Dashboard available at:* `http://localhost:8501`

## 🔗 API & Data Reference

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tickets` | Create a new ticket |
| `GET` | `/tickets` | Retrieve all tickets |
| `GET` | `/tickets/{ticket_id}` | Fetch a specific ticket by ID |
| `PATCH` | `/tickets/{ticket_id}/status` | Update a ticket's status |

### Ticket Classification Example
**POST `/tickets` Input:**
```json
{
  "id": "TKT001",
  "title": "Office Internet Failure",
  "description": "Entire office internet is unavailable"
}
```
**Auto-Generated Response:**
```json
{
  "category": "NETWORK",
  "priority": "CRITICAL",
  "status": "OPEN"
}
```

### Supported Data Enums
*   **Categories:** `HARDWARE`, `NETWORK`, `SECURITY`, `SOFTWARE`
*   **Statuses:** `OPEN`, `PENDING`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`
*   **Priorities:** 
    *   `CRITICAL` (Major disruption) | `HIGH` (Significant impact) | `MEDIUM` (Moderate) | `LOW` (Minor)

## 🔐 Security Note
*   **Status:** Demonstration & Learning build. 
*   **Current State:** While the dashboard interface requires an admin login, the backend API endpoints do not currently enforce authentication. Do not use this version in production deployments.

***
**Author:** Hariharan

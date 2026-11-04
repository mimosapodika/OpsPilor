# 🎫 OpsPilot — IT Support Ticket Management System

OpsPilot is a lightweight IT Support Ticket Management System that helps organizations create, classify, track, and manage IT support requests.

It automatically classifies incoming tickets based on their descriptions, assigns priority levels, and provides an interactive dashboard for monitoring and managing tickets.

## 🚀 Features

- **Automatic Ticket Classification:** Classifies tickets into Hardware, Network, Security, and Software categories using a Python rule-based classifier.
- **Priority Detection:** Automatically assigns Critical, High, Medium, or Low priority.
- **Ticket Management:** Create and store support tickets using a REST API.
- **Interactive Dashboard:** Monitor total tickets, open tickets, critical tickets, and category distribution.
- **Priority-Based Sorting:** Displays critical and high-priority tickets before lower-priority tickets.
- **Ticket Search:** Search for individual tickets using their unique IDs.
- **Administrator Controls:** Login interface for administrators to update ticket statuses.
- **Persistent Storage:** Stores ticket information using SQLite.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | REST API backend |
| SQLite | Database |
| Streamlit | Interactive dashboard |
| Requests | API communication |
| Uvicorn | API server |
| Git & GitHub | Version control |

## 🏗️ System Architecture

```text
             User
              |
              v
     Streamlit Dashboard
              |
              v
        FastAPI Backend
              |
       +------+------+
       |             |
       v             v
  Rule-Based      SQLite
  Classifier      Database
       |             |
       +------+------+
              |
              v
       Ticket Management
```

## 📂 Project Structure

```text
OpsPilot/
│
├── src/
│   └── opspilot/
│       ├── __init__.py
│       ├── api.py
│       ├── classifier.py
│       ├── database.py
│       ├── manager.py
│       └── models.py
│
├── .streamlit/
│   └── secrets.toml
│
├── dashboard.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

The SQLite database is created locally when the application initializes.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mimosapodika/OpsPilor.git
cd OpsPilor
```

### 2. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if it is not already installed.

```bash
uv sync
```

### 3. Configure administrator credentials

Create a `.streamlit` folder in the project root and create a `secrets.toml` file inside it.

Add:

```toml
[admin]
username = "admin"
password = "YOUR_PRIVATE_PASSWORD"
```

Replace the example password with your own.

**Important:** Never upload `secrets.toml` to GitHub.

### 4. Start the FastAPI backend

Open a terminal in the project directory:

```bash
uv run uvicorn opspilot.api:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### 5. Start the Streamlit dashboard

Open a second terminal in the project directory.

For Windows PowerShell:

```powershell
$env:STREAMLIT_CONFIG_DIR = (Join-Path (Get-Location).Path ".streamlit")

uv run streamlit run dashboard.py --server.headless true --browser.gatherUsageStats false
```

Open the dashboard:

http://localhost:8501

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tickets` | Create a new ticket |
| GET | `/tickets` | Retrieve all tickets |
| GET | `/tickets/{ticket_id}` | Search for a ticket by ID |
| PATCH | `/tickets/{ticket_id}/status` | Update ticket status |

### Ticket Classification Example

**Input:**

```json
{
  "id": "TKT001",
  "title": "Office Internet Failure",
  "description": "Entire office internet is unavailable"
}
```

**Expected classification:**

```json
{
  "category": "NETWORK",
  "priority": "CRITICAL"
}
```

The created ticket is stored in SQLite with its status initially set to `OPEN`.

## 📊 Ticket Categories

- HARDWARE
- NETWORK
- SECURITY
- SOFTWARE

## 🚦 Priority Levels

| Priority | Description |
|---|---|
| CRITICAL | Major organizational disruption |
| HIGH | Significant issue affecting work |
| MEDIUM | Moderate or intermittent issue |
| LOW | Minor issue |

## 📌 Ticket Statuses

- OPEN
- PENDING
- IN_PROGRESS
- RESOLVED
- CLOSED

Administrators can update ticket statuses through the dashboard.

## 🔐 Security Note

The current administrator login protects the dashboard interface. The status-update API endpoint does not yet enforce backend authentication, so this version is intended for local demonstration and learning rather than production deployment.

Administrator credentials are stored locally in Streamlit secrets and should never be committed to the repository.

## 🎯 Project Objective

The objective of OpsPilot is to simplify IT support ticket handling by automating initial ticket classification, prioritizing important issues, and providing a centralized interface for monitoring and managing support requests.

## 👨‍💻 Author

Developed as a software engineering portfolio project to explore backend development, REST APIs, database integration, automation, and dashboard development.

---

**OpsPilot — Making IT Support Management Simpler.**

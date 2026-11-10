# OpsPilot 🛠️

An AI-powered IT Support Ticket Management and Triage System built with **FastAPI**, **Streamlit**, and **Groq (Llama 3.3)**, designed for lightning-fast issue resolution and administrative control.
---
## 🚀 Features
* **Automated Ticket Triage:** Instantly classifies tickets by category (`SOFTWARE`, `HARDWARE`, etc.) and sets priority                                    levels (`LOW`, `MEDIUM`, `HIGH`).
* **Groq AI Troubleshooting:** Automatically feeds ticket descriptions to Groq (`openai/gpt-oss-120b`) to generate                                          actionable, 1–2 sentence resolution guides and root-cause analysis for IT staff.
* **REST API Backend:** Fully asynchronous and robust FastAPI service with SQLite persistence and Pydantic validation.
* **Interactive Employee Dashboard:** Streamlit UI allowing users to submit tickets, view real-time status updates, and                                            inspect live AI troubleshooting insights.
* **Admin Control Panel:** Secured status updater to manage ticket lifecycles (`OPEN` $\rightarrow$ `IN_PROGRESS`  $\rightarrow$ `RESOLVED` $\rightarrow$ `CLOSED`).
* 
---
** 📦 Tech Stack **
* **Backend:** Python, FastAPI, Pydantic, SQLite, `uv`
* **Frontend:** Streamlit (`dashboard.py`)
* **AI Engine:** Groq API (`openai/gpt-oss-120b`)
* **Environment Manager:** `uv`
---
## ⚙️ Quick Start & Installation

### 1. Clone & Set Up Environment
powershell
git clone [https://github.com/mimosapodika/OpsPilor.git](https://github.com/mimosapodika/OpsPilor.git)
cd OpsPilor 

** 2. Set your Groq API key in your terminal session: **
PowerShell
$env:GROQ_API_KEY="gsk_YourActualGroqApiKeyHere"

3. Run the FastAPI Backend
PowerShell
$env:PYTHONPATH="src"
uv run uvicorn opspilot.api:app --reload

4.Launch the Streamlit Dashboard (In a Second Terminal)
PowerShell
uv run streamlit run dashboard.py --server.headless=true --browser.gatherUsageStats=fale

** Project structure ** 
OpsPilor/
├── src/
│   └── opspilot/
│       ├── __init__.py
│       ├── ai_helper.py       # Groq API integration & prompt logic
│       ├── api.py             # FastAPI REST endpoints & routes
│       ├── classifier.py      # Rule-based fallback classification
│       ├── database.py        # SQLite initialization & schema
│       ├── manager.py         # Ticket CRUD operations
│       └── models.py          # Pydantic data models
├── dashboard.py               # Streamlit employee & admin UI
└── pyproject.toml             # Dependency management (`uv`)

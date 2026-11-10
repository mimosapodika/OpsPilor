import streamlit as st
import requests

# Streamlit Page Configuration
st.set_page_config(
    page_title="OpsPilot - IT Support Ticket Management",
    page_icon="🛠️",
    layout="wide"
)

# API Endpoint Configuration
API_URL = "http://127.0.0.1:8000"

st.title("🛠️ OpsPilot IT Support Dashboard")
st.markdown("Manage, track, and triage support tickets augmented with Groq AI intelligence.")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["View Tickets", "Create New Ticket", "Admin Panel"])

# --- VIEW TICKETS PAGE ---
if page == "View Tickets":
    st.header("📋 Support Tickets")

    if st.button("Refresh Tickets"):
        st.rerun()

    try:
        response = requests.get(f"{API_URL}/tickets", timeout=5)
        if response.status_code == 200:
            tickets = response.json()
            if not tickets:
                st.info("No tickets found in the system yet. Create one using the sidebar!")
            else:
                for ticket in tickets:
                    with st.expander(f"[{ticket.get('id')}] {ticket.get('title')} — Priority: {ticket.get('priority', 'MEDIUM')} | Status: {ticket.get('status', 'OPEN')}"):
                        st.write(f"**Description:** {ticket.get('description')}")
                        st.write(f"**Category:** {ticket.get('category', 'SOFTWARE')}")
                        st.write(f"**Status:** {ticket.get('status', 'OPEN')}")
                        st.write(f"**Created At:** {ticket.get('created_at', 'N/A')}")
        else:
            st.error("Failed to fetch tickets from the OpsPilot API.")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the OpsPilot API. Make sure FastAPI is running on port 8000.")

# --- CREATE NEW TICKET PAGE ---
elif page == "Create New Ticket":
    st.header("🎫 Create a New Support Ticket")

    with st.form("ticket_form"):
        ticket_id = st.text_input("Ticket ID (e.g., T01, T02)", value="")
        title = st.text_input("Issue Title", value="")
        description = st.text_area("Issue Description (Describe technical problems in detail for AI analysis)", value="")

        submitted = st.form_submit_button("Submit Ticket")

    if submitted:
        if not ticket_id.strip() or not title.strip() or not description.strip():
            st.warning("Please fill in all three fields.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/tickets",
                    json={
                        "id": ticket_id,
                        "title": title,
                        "description": description
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success(
                        f"Ticket created successfully! Category: {result.get('category')} | "
                        f"Priority: {result.get('priority')}"
                    )

                    # Display Groq AI Troubleshooting Insights
                    if "ai_insights" in result:
                        with st.expander("🤖 Groq AI Troubleshooting Insight", expanded=True):
                            st.write(result["ai_insights"])
                else:
                    st.error(f"Failed to create ticket: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the OpsPilot API. Make sure FastAPI is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# --- ADMIN PANEL PAGE ---
elif page == "Admin Panel":
    st.header("🔐 Admin Panel: Ticket Management & Status Control")

    try:
        response = requests.get(f"{API_URL}/tickets", timeout=5)
        if response.status_code == 200:
            tickets = response.json()
            if not tickets:
                st.info("No tickets available to manage.")
            else:
                ticket_ids = [t["id"] for t in tickets]

                with st.form("status_update_form"):
                    selected_id = st.selectbox("Select Ticket ID to Update", options=ticket_ids)

                    # Find current status of selected ticket
                    current_status = next((t["status"] for t in tickets if t["id"] == selected_id), "OPEN")
                    status_options = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]
                    default_idx = status_options.index(current_status) if current_status in status_options else 0

                    new_status = st.selectbox("New Status", options=status_options, index=default_idx)

                    update_submitted = st.form_submit_button("Update Ticket Status")

                if update_submitted:
                    update_response = requests.patch(
                        f"{API_URL}/tickets/{selected_id}/status",
                        json={"status": new_status},
                        timeout=5
                    )
                    if update_response.status_code == 200:
                        st.success(f"Ticket {selected_id} status successfully updated to {new_status}!")
                        st.rerun()
                    else:
                        st.error(f"Failed to update status: {update_response.text}")
        else:
            st.error("Failed to load tickets for admin panel.")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the OpsPilot API. Make sure FastAPI is running on port 8000.")

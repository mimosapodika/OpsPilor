
import streamlit as st
import requests

st.set_page_config(
    page_title="OpsPilot",
    page_icon="🎫",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

# Administrator authentication

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

def admin_login():
    st.session_state.admin_logged_in = True

def admin_logout():
    st.session_state.admin_logged_in = False



st.title("🎫 OpsPilot")
st.subheader("IT Support Ticket Management System")

st.divider()

# Create a new support ticket
st.subheader("➕ Create New Ticket")

with st.form("create_ticket_form"):
    ticket_id = st.text_input("Ticket ID")
    title = st.text_input("Ticket Title")
    description = st.text_area("Describe the issue")

    submitted = st.form_submit_button("Create Ticket")

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

            if response.status_code == 409:
                st.error("This Ticket ID already exists. Use a different ID.")

            else:
                response.raise_for_status()
                created_ticket = response.json()

                st.success(
                    f"Ticket created! Category: {created_ticket['category']} | "
                    f"Priority: {created_ticket['priority']}"
                )

        except requests.exceptions.RequestException as error:
            st.error("Unable to create the ticket.")
            st.caption(str(error))

st.divider()

# Fetch tickets from FastAPI
try: 
    response = requests.get(
        f"{API_URL}/tickets",
        timeout=10
    )

    response.raise_for_status()

    tickets = response.json()

    # Dashboard statistics
    total_tickets = len(tickets)

    open_tickets = sum(
        1 for ticket in tickets
        if ticket["status"] == "OPEN"
    )

    critical_tickets = sum(
        1 for ticket in tickets
        if ticket["priority"] == "CRITICAL"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Critical Tickets", critical_tickets)

    st.divider()

    # Category summary
    st.subheader("Tickets by Category")

    categories = ["HARDWARE", "NETWORK", "SECURITY", "SOFTWARE"]

    category_counts = {
        category: sum(
            1 for ticket in tickets
            if ticket["category"] == category
        )
        for category in categories
    }

    st.bar_chart(category_counts)

    st.divider()

    # Ticket table
    
    # Ticket table
    st.subheader("All Support Tickets")

    if tickets:
        priority_order = {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        }

        sorted_tickets = sorted(
            tickets,
            key=lambda ticket: priority_order.get(
                ticket["priority"], 5
            )
        )

        st.dataframe(
            sorted_tickets,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No tickets have been created yet.")

except requests.exceptions.RequestException as error:
    st.error("Unable to connect to the OpsPilot API.")
    st.caption(str(error))

st.divider()
st.subheader("🔐 Administrator Access")

if not st.session_state.admin_logged_in:

    with st.form("admin_login_form"):
        username = st.text_input("Admin Username")
        password = st.text_input(
            "Admin Password",
            type="password"
        )

        login_submitted = st.form_submit_button("Login")

        if login_submitted:
            if (
                username == st.secrets["admin"]["username"]
                and password == st.secrets["admin"]["password"]
            ):
                admin_login()
                st.rerun()
            else:
                st.error("Invalid username or password.")

else:
    st.success("Administrator logged in.")

    if st.button("Logout"):
        admin_logout()
        st.rerun()

    st.subheader("Update Ticket Status")

    with st.form("update_ticket_status_form"):
        update_id = st.text_input("Ticket ID")

        new_status = st.selectbox(
            "New Status",
            ["OPEN", "PENDING", "IN_PROGRESS", "RESOLVED", "CLOSED"]
        )

        update_submitted = st.form_submit_button("Update Status")

        if update_submitted:
            if not update_id.strip():
                st.warning("Enter a Ticket ID.")
            else:
                try:
                    response = requests.patch(
                        f"{API_URL}/tickets/{update_id.strip()}/status",
                        json={"status": new_status},
                        timeout=10
                    )

                    if response.status_code == 200:
                        st.success("Ticket status updated!")
                        st.json(response.json())
                        st.rerun()

                    elif response.status_code == 404:
                        st.error("Ticket not found.")

                    else:
                        st.error(response.text)

                except requests.exceptions.RequestException:
                    st.error("Unable to connect to API.")

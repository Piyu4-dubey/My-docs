import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="IT Support Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state — UI code must be OUTSIDE this block
if 'tech_tickets' not in st.session_state:
    st.session_state.tech_tickets = [
        {
            "Ticket ID": "TKT-1001",
            "User": "John Smith",
            "Email": "john.smith@company.com",
            "Department": "Marketing",
            "Title": "New Laptop Required",
            "Category": "Hardware",
            "Priority": "High",
            "Status": "Pending Approval",
            "Description": "Need a new MacBook Pro for video editing work. Current laptop is 5 years old.",
            "Created": "2024-02-13 10:30",
            "Requested Item": "MacBook Pro 16-inch M3",
            "Collection Time": None,
            "Assigned Tech": None,
            "Notes": ""
        }
    ]

# --- Header (outside session state block so it always renders) ---
st.title("IT Support Dashboard")
st.subheader("Raise and Manage Tickets")
st.divider()

# --- Metrics ---
col1, col2, col3 = st.columns(3)
pending_count  = len([t for t in st.session_state.tech_tickets if t["Status"] == "Pending Approval"])
approved_count = len([t for t in st.session_state.tech_tickets if t["Status"] == "Approved"])
rejected_count = len([t for t in st.session_state.tech_tickets if t["Status"] == "Rejected"])

with col1:
    st.metric("Pending Approval", pending_count)
with col2:
    st.metric("Approved", approved_count)
with col3:
    st.metric("Rejected", rejected_count)

st.divider()

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Pending", "Approved", "Rejected"])

# ── Tab 1: Pending ──────────────────────────────────────────────
with tab1:
    st.header("Pending Requests")
    pending_tickets = [t for t in st.session_state.tech_tickets if t["Status"] == "Pending Approval"]

    if pending_tickets:
        for ticket in pending_tickets:
            with st.container(border=True):
                # Title row
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(ticket["Title"])
                    st.caption(f"**ID:** {ticket['Ticket ID']} | **User:** {ticket['User']}")
                with col2:
                    if ticket["Priority"] == "High":
                        st.error(ticket["Priority"])
                    elif ticket["Priority"] == "Medium":
                        st.warning(ticket["Priority"])
                    else:
                        st.success(ticket["Priority"])

                # Details — kept inside the container block
                st.write(f"**Description:** {ticket['Description']}")
                st.write(f"**Requested Item:** {ticket['Requested Item']}")
                st.write(f"**Created:** {ticket['Created']}")

                # Approve / Reject buttons per ticket
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("✅ Approve", key=f"approve_{ticket['Ticket ID']}"):
                        ticket["Status"] = "Approved"
                        st.success("Ticket approved!")
                        st.rerun()
                with btn_col2:
                    if st.button("❌ Reject", key=f"reject_{ticket['Ticket ID']}"):
                        ticket["Status"] = "Rejected"
                        st.error("Ticket rejected.")
                        st.rerun()
    else:
        st.info("No pending tickets.")

# ── Tab 2: Approved ─────────────────────────────────────────────
with tab2:
    st.header("Approved Tickets")
    # FIX: was checking "Approved Ticket" — corrected to "Approved"
    approved_tickets = [t for t in st.session_state.tech_tickets if t["Status"] == "Approved"]

    if approved_tickets:
        for ticket in approved_tickets:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(ticket["Title"])
                    st.caption(f"**ID:** {ticket['Ticket ID']} | **User:** {ticket['User']}")
                with col2:
                    st.success("Approved")
                st.write(f"**Description:** {ticket['Description']}")
                st.write(f"**Requested Item:** {ticket['Requested Item']}")
                st.write(f"**Created:** {ticket['Created']}")
    else:
        st.info("No approved tickets yet.")

# ── Tab 3: Rejected ─────────────────────────────────────────────
with tab3:
    st.header("Rejected Tickets")
    rejected_tickets = [t for t in st.session_state.tech_tickets if t["Status"] == "Rejected"]

    if rejected_tickets:
        for ticket in rejected_tickets:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(ticket["Title"])
                    st.caption(f"**ID:** {ticket['Ticket ID']} | **User:** {ticket['User']}")
                with col2:
                    st.error("Rejected")
                st.write(f"**Description:** {ticket['Description']}")
                st.write(f"**Requested Item:** {ticket['Requested Item']}")
                st.write(f"**Created:** {ticket['Created']}")
    else:
        st.info("No rejected tickets.")
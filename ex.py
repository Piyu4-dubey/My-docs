import streamlit as st
from streamlit_searchbox import st_searchbox
import pandas as pd

# 1. INITIALIZATION
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False
if 'tickets' not in st.session_state:
    st.session_state.tickets = [] 

# Function to toggle form
def create_ticket(status):
    st.session_state.show_create_form = status

# --- HEADER SECTION ---
st.markdown("<h3 style='text-align: left; color: blue;'>IT SUPPORT HELP DESK</h3>", unsafe_allow_html=True)

# TOP BUTTONS
col_left, col_right = st.columns([2, 1], gap="medium")
with col_right:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("Create Ticket", type="primary", on_click=create_ticket, args=(True,), use_container_width=True)
    with btn_col2:
        st.button("View Tickets", type="primary", on_click=create_ticket, args=(False,), use_container_width=True)

# TICKET STATUS FILTER
options = ["Open Ticket", "In Progress", "Closed Ticket"]
selection = st.segmented_control("Ticket status:", options, selection_mode="single", default="Open Ticket")

# 5. CREATE TICKET FORM
if st.session_state.show_create_form:
    st.divider()
    with st.form("New Ticket form", clear_on_submit=True):
        name = st.text_input("Confirm your name", value="User")
        st.subheader(f"Hi {name}, how can I assist you today?")
    
        issue_title = st.text_input("Enter issue title")
        category = st.selectbox("Category", ["Software", "Hardware", "Network", "LMS Approval"])
        priority = st.pills("Select Priority Level:", options=["High", "Medium", "Low"], default="Medium")
        description = st.text_area("Provide Detail Description")

        col_submit, col_clear = st.columns([4, 1])
        with col_submit:
            submitted = st.form_submit_button("Submit Ticket", type="primary", use_container_width=True)
        with col_clear:
            st.form_submit_button("Clear")

        if submitted:
            if issue_title and description:
                # --- SAVE DATA ---
                new_ticket = {
                    "User": name,
                    "Title": issue_title,
                    "Category": category,
                    "Priority": priority,
                    "Status": "Open Ticket",
                    "Description": description
                }
                st.session_state.tickets.append(new_ticket)
                st.success(f"Ticket Created! Priority set to {priority}")
                st.session_state.show_create_form = False
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

# 6. VIEW TICKETS (Now correctly outside the form block)
else:
    st.divider()
    st.subheader(f"Dashboard: {selection}")

    if st.session_state.tickets:
        df = pd.DataFrame(st.session_state.tickets)
        # Filter based on the segmented control
        filtered_df = df[df['Status'] == selection]

        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No tickets currently marked as '{selection}'")
    else:
        st.info("No tickets created yet. Click 'Create Ticket' to start.")

# 7. SIDEBAR SECTION
def search_function(search_term: str) -> list:
    suggestions = ["Laptop issue", "charger issue", "Access to lms"]
    return [item for item in suggestions if search_term.lower() in item.lower()] if search_term else suggestions

with st.sidebar:
    st.title("My Tickets")
    selected = st_searchbox(search_function, key="sidebar_search", placeholder="search recent issue")

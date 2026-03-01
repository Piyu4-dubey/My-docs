import streamlit as st
from streamlit_searchbox import st_searchbox
import pandas as pd
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="IT Support Help Desk",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: #e0e7ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 4px solid;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card.open {
        border-left-color: #f59e0b;
    }
    
    .metric-card.progress {
        border-left-color: #3b82f6;
    }
    
    .metric-card.closed {
        border-left-color: #10b981;
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Form styling */
    .stForm {
        background: #f9fafb;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
    }
    
    /* Priority badges */
    .priority-high {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
    }
    
    .priority-medium {
        background: #fef3c7;
        color: #d97706;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
    }
    
    .priority-low {
        background: #d1fae5;
        color: #059669;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] h1 {
        color: white;
    }
    
    /* Button animations */
    .stButton button {
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Ticket card */
    .ticket-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Icon styling */
    .icon-text {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# INITIALIZATION
if 'show_create_form' not in st.session_state:
    st.session_state.show_create_form = False
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
if 'ticket_counter' not in st.session_state:
    st.session_state.ticket_counter = 1000

# Function to toggle form
def create_ticket(status):
    st.session_state.show_create_form = status

# --- ANIMATED HEADER ---
st.markdown("""
<div class="main-header">
    <h1> IT Support Help Desk</h1>
    <p>Your one-stop solution for all IT issues | Fast • Reliable • 24/7</p>
</div>
""", unsafe_allow_html=True)

# --- METRICS DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_tickets = len(st.session_state.tickets)
open_tickets = len([t for t in st.session_state.tickets if t['Status'] == 'Open Ticket'])
in_progress = len([t for t in st.session_state.tickets if t['Status'] == 'In Progress'])
closed_tickets = len([t for t in st.session_state.tickets if t['Status'] == 'Closed Ticket'])

with col1:
    st.metric(
        label=" Total Tickets",
        value=total_tickets,
        delta=f"+{total_tickets}" if total_tickets > 0 else "0"
    )

with col2:
    st.metric(
        label="Open Tickets",
        value=open_tickets,
        delta=f"{open_tickets} pending"
    )

with col3:
    st.metric(
        label=" In Progress",
        value=in_progress,
        delta="Active" if in_progress > 0 else "None"
    )

with col4:
    st.metric(
        label="Closed",
        value=closed_tickets,
        delta=f"{closed_tickets} resolved"
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- ACTION BUTTONS ---
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Create New Ticket", type="primary", on_click=create_ticket, args=(True,), use_container_width=True):
            pass
    with btn_col2:
        if st.button("View All Tickets", type="secondary", on_click=create_ticket, args=(False,), use_container_width=True):
            pass

st.markdown("<br>", unsafe_allow_html=True)

# --- TICKET STATUS FILTER ---
st.markdown("### Filter Tickets by Status")
options = ["Open Ticket", "In Progress", "Closed Ticket"]
selection = st.segmented_control(
    "Ticket status:",
    options,
    selection_mode="single",
    default="Open Ticket",
    label_visibility="collapsed"
)

# --- CREATE TICKET FORM ---
if st.session_state.show_create_form:
    st.markdown("---")
    st.markdown("###  Create New Support Ticket")
    
    with st.form("New Ticket form", clear_on_submit=True):
        # User greeting
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input("Your Name", value="", placeholder="Enter your full name")
        with col2:
            email = st.text_input("Email", placeholder="your.email@company.com")
        
        if name:
            st.markdown(f"### Hi **{name}**, how can we assist you today?")
        else:
            st.markdown("###  How can we assist you today?")
        
        # Ticket details
        col1, col2 = st.columns(2)
        with col1:
            issue_title = st.text_input("Issue Title", placeholder="Brief description of the issue")
            category = st.selectbox(
                " Category",
                ["Software", "Hardware", "Network", "LMS Approval", "Email Issues", "Printer", "Other"],
                index=0
            )
        with col2:
            priority = st.selectbox(
                "Priority Level",
                ["High", "Medium", "Low"],
                index=1
            )
            department = st.selectbox(
                "Department",
                ["IT", "HR", "Finance", "Operations", "Sales", "Marketing"],
                index=0
            )
        
        description = st.text_area(
            "Detailed Description",
            placeholder="Please provide a detailed description of your issue...",
            height=150
        )
        
        # Attachment (placeholder)
        uploaded_file = st.file_uploader("📎 Attach Screenshot/File (optional)", type=['png', 'jpg', 'pdf', 'docx'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit buttons
        col_submit, col_clear, col_cancel = st.columns([2, 1, 1])
        with col_submit:
            submitted = st.form_submit_button(" Submit Ticket", type="primary", use_container_width=True)
        with col_clear:
            st.form_submit_button(" Clear", use_container_width=True)
        with col_cancel:
            cancel = st.form_submit_button(" Cancel", use_container_width=True)

        if submitted:
            if name and issue_title and description:
                # Generate ticket ID
                ticket_id = f"TKT-{st.session_state.ticket_counter}"
                st.session_state.ticket_counter += 1
                
                # Save ticket
                new_ticket = {
                    "Ticket ID": ticket_id,
                    "User": name,
                    "Email": email if email else "N/A",
                    "Title": issue_title,
                    "Category": category,
                    "Department": department,
                    "Priority": priority,
                    "Status": "Open Ticket",
                    "Description": description,
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Attachment": uploaded_file.name if uploaded_file else "None"
                }
                st.session_state.tickets.append(new_ticket)
                
                # Success message
                st.balloons()
                st.success(f" Ticket Created Successfully! Ticket ID: **{ticket_id}** | Priority: **{priority}**")
                st.info("Our support team will get back to you shortly. Please check your email for updates.")
                
                st.session_state.show_create_form = False
                st.rerun()
            else:
                st.error(" Please fill in all required fields (Name, Issue Title, and Description)")
        
        if cancel:
            st.session_state.show_create_form = False
            st.rerun()

# --- VIEW TICKETS ---
else:
    st.markdown("---")
    st.markdown(f"###  Ticket Dashboard: **{selection}**")
    
    if st.session_state.tickets:
        df = pd.DataFrame(st.session_state.tickets)
        
        # Filter based on selection
        filtered_df = df[df['Status'] == selection]
        
        if not filtered_df.empty:
            # Display options
            view_mode = st.radio(
                "View Mode:",
                ["Table View", "Card View"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if view_mode == "Table View":
                # Enhanced dataframe display
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Ticket ID": st.column_config.TextColumn("Ticket ID", width="small"),
                        "User": st.column_config.TextColumn(" User", width="medium"),
                        "Title": st.column_config.TextColumn(" Title", width="large"),
                        "Priority": st.column_config.TextColumn(" Priority", width="small"),
                        "Category": st.column_config.TextColumn(" Category", width="small"),
                        "Status": st.column_config.TextColumn(" Status", width="medium"),
                        "Created": st.column_config.TextColumn(" Created", width="medium")
                    }
                )
            else:
                # Card View
                for idx, ticket in filtered_df.iterrows():
                    priority_color = {
                        "High": "🔴",
                        "Medium": "🟡",
                        "Low": "🟢"
                    }
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="ticket-card">
                            <h4>{priority_color.get(ticket['Priority'], )} {ticket['Title']}</h4>
                            <p><strong>Ticket ID:</strong> {ticket['Ticket ID']} | 
                               <strong>User:</strong> {ticket['User']} | 
                               <strong>Priority:</strong> <span class="priority-{ticket['Priority'].lower()}">{ticket['Priority']}</span></p>
                            <p><strong>Category:</strong> {ticket['Category']} | 
                               <strong>Department:</strong> {ticket.get('Department', 'N/A')} | 
                               <strong>Created:</strong> {ticket['Created']}</p>
                            <p><strong>Description:</strong> {ticket['Description'][:100]}...</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Action buttons for each ticket
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                        with col1:
                            if st.button(" View", key=f"view_{idx}"):
                                st.info(f"Viewing details for {ticket['Ticket ID']}")
                        with col2:
                            if st.button(" Edit", key=f"edit_{idx}"):
                                st.info(f"Editing {ticket['Ticket ID']}")
                        with col3:
                            if st.button("Close", key=f"close_{idx}"):
                                st.success(f"Closed {ticket['Ticket ID']}")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info(f"No tickets currently marked as **'{selection}'**. All caught up! 🎉")
    else:
        st.info(" No tickets created yet. Click **'Create New Ticket'** to get started!")
        
      

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("###  Quick Search")
    
    def search_function(search_term: str) -> list:
        suggestions = [
            " Laptop not starting",
            " Charger issue",
            " Access to LMS",
            " Printer not working",
            " Email configuration",
            " Network connectivity",
            " Password reset",
            " Software installation"
        ]
        return [item for item in suggestions if search_term.lower() in item.lower()] if search_term else suggestions
    
    selected = st_searchbox(
        search_function,
        key="sidebar_search",
        placeholder=" Search tickets or issues..."
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("###  Quick Stats")
    st.markdown(f"""
    - **Total Tickets:** {total_tickets}
    - **Pending:** {open_tickets}
    - **Active:** {in_progress}
    - **Resolved:** {closed_tickets}
    """)
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("###  Recent Activity")
    if st.session_state.tickets:
        recent_tickets = st.session_state.tickets[-3:][::-1]  # Last 3 tickets
        for ticket in recent_tickets:
            st.markdown(f"**{ticket['Ticket ID']}** - {ticket['Title'][:30]}...")
    else:
        st.markdown("*No recent activity*")
    
    st.markdown("---")
    
    
    
    st.markdown("---")
    st.markdown("*Powered by IT Help Desk *")
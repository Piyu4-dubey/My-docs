import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# PAGE CONFIG
st.set_page_config(
    page_title="IT Support Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INITIALIZE SESSION STATE
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
        },
        {
            "Ticket ID": "TKT-1002",
            "User": "Sarah Johnson",
            "Email": "sarah.j@company.com",
            "Department": "Finance",
            "Title": "External Monitor Setup",
            "Category": "Hardware",
            "Priority": "Medium",
            "Status": "In Progress",
            "Description": "Need dual monitor setup for financial analysis work",
            "Created": "2024-02-13 09:15",
            "Requested Item": "Dell 27-inch Monitor x2",
            "Collection Time": "2024-02-15 14:00",
            "Assigned Tech": "Mike Chen",
            "Notes": "Monitors ordered, arriving tomorrow"
        },
        {
            "Ticket ID": "TKT-1003",
            "User": "David Lee",
            "Email": "dlee@company.com",
            "Department": "IT",
            "Title": "Wireless Mouse and Keyboard",
            "Category": "Hardware",
            "Priority": "Low",
            "Status": "Approved",
            "Description": "Ergonomic keyboard and mouse for new workstation",
            "Created": "2024-02-12 16:45",
            "Requested Item": "Logitech MX Keys + MX Master 3",
            "Collection Time": "2024-02-14 10:00",
            "Assigned Tech": "You",
            "Notes": "Ready for pickup from IT room"
        }
    ]

# Initialize inventory in session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"Item": "Laptops", "Total Stock": 63, "Available": 15, "Assigned": 45, "In Repair": 3},
        {"Item": "Monitors", "Total Stock": 92, "Available": 23, "Assigned": 67, "In Repair": 2},
        {"Item": "Keyboards", "Total Stock": 113, "Available": 34, "Assigned": 78, "In Repair": 1},
        {"Item": "Mice", "Total Stock": 120, "Available": 38, "Assigned": 82, "In Repair": 0},
        {"Item": "Chargers", "Total Stock": 85, "Available": 25, "Assigned": 55, "In Repair": 5},
        {"Item": "Headsets", "Total Stock": 45, "Available": 12, "Assigned": 31, "In Repair": 2},
        {"Item": "Webcams", "Total Stock": 38, "Available": 15, "Assigned": 21, "In Repair": 2},
        {"Item": "Docking Stations", "Total Stock": 28, "Available": 8, "Assigned": 19, "In Repair": 1}
    ]

# HEADER
st.title("⚙️ IT Support Dashboard")
st.subheader("Manage Hardware Requests & Track Tickets")
st.divider()

# METRICS ROW
col1, col2, col3, col4 = st.columns(4)

pending_count = len([t for t in st.session_state.tech_tickets if t['Status'] == 'Pending Approval'])
in_progress_count = len([t for t in st.session_state.tech_tickets if t['Status'] == 'In Progress'])
approved_count = len([t for t in st.session_state.tech_tickets if t['Status'] == 'Approved'])
completed_count = len([t for t in st.session_state.tech_tickets if t['Status'] == 'Completed'])

with col1:
    st.metric("⏳ Pending", pending_count)

with col2:
    st.metric("🔧 In Progress", in_progress_count)

with col3:
    st.metric("✅ Approved", approved_count)

with col4:
    st.metric("✔️ Completed", completed_count)

st.divider()

# MAIN TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Pending Requests",
    "🔧 Active Tickets",
    "📊 All Tickets",
    "📦 Inventory"
])

# ============= TAB 1: PENDING REQUESTS =============
with tab1:
    st.header("⏳ Pending Approval")
    
    pending_tickets = [t for t in st.session_state.tech_tickets if t['Status'] == 'Pending Approval']
    
    if pending_tickets:
        for ticket in pending_tickets:
            with st.container(border=True):
                # Header row
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{ticket['Title']}")
                    st.caption(f"**ID:** {ticket['Ticket ID']} | **User:** {ticket['User']} | **Dept:** {ticket['Department']}")
                with col2:
                    if ticket['Priority'] == 'High':
                        st.error(f" {ticket['Priority']}")
                    elif ticket['Priority'] == 'Medium':
                        st.warning(f"{ticket['Priority']}")
                    else:
                        st.success(f" {ticket['Priority']}")
                
                # Details
                st.write(f"**Description:** {ticket['Description']}")
                st.write(f"**Requested Item:** {ticket['Requested Item']}")
                st.write(f"**Created:** {ticket['Created']}")
                
                st.divider()
                
                # Action Section
                with st.expander("🎯 Approve or Reject", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### ✅ Approve")
                        assigned_tech = st.selectbox(
                            "Assign to",
                            ["You", "Mike Chen", "Sarah Williams", "James Brown"],
                            key=f"tech_{ticket['Ticket ID']}"
                        )
                        
                        collection_date = st.date_input(
                            "Collection Date",
                            value=datetime.now() + timedelta(days=2),
                            key=f"date_{ticket['Ticket ID']}"
                        )
                        
                        collection_time = st.time_input(
                            "Collection Time",
                            value=datetime.strptime("14:00", "%H:%M").time(),
                            key=f"time_{ticket['Ticket ID']}"
                        )
                        
                        notes = st.text_area(
                            "Notes",
                            placeholder="Add notes...",
                            key=f"notes_{ticket['Ticket ID']}"
                        )
                        
                        if st.button(f"✅ Approve Request", type="primary", key=f"approve_{ticket['Ticket ID']}", use_container_width=True):
                            for t in st.session_state.tech_tickets:
                                if t['Ticket ID'] == ticket['Ticket ID']:
                                    t['Status'] = 'Approved'
                                    t['Assigned Tech'] = assigned_tech
                                    t['Collection Time'] = f"{collection_date} {collection_time}"
                                    t['Notes'] = notes
                            
                            st.success(f"✅ Approved! Collection: {collection_date} at {collection_time}")
                            st.balloons()
                            st.rerun()
                    
                    with col2:
                        st.markdown("#### ❌ Reject")
                        rejection_reason = st.selectbox(
                            "Reason",
                            ["Out of Stock", "Budget Issue", "Policy Violation", "Other"],
                            key=f"reject_reason_{ticket['Ticket ID']}"
                        )
                        
                        rejection_notes = st.text_area(
                            "Explanation",
                            placeholder="Why rejected...",
                            key=f"reject_notes_{ticket['Ticket ID']}"
                        )
                        
                        if st.button(f"❌ Reject Request", key=f"reject_{ticket['Ticket ID']}", use_container_width=True):
                            for t in st.session_state.tech_tickets:
                                if t['Ticket ID'] == ticket['Ticket ID']:
                                    t['Status'] = 'Rejected'
                                    t['Notes'] = f"Rejected: {rejection_reason} - {rejection_notes}"
                            
                            st.warning(f"❌ Request rejected")
                            st.rerun()
    else:
        st.info("✨ No pending requests")

# ============= TAB 2: ACTIVE TICKETS =============
with tab2:
    st.header("🔧 Active Tickets")
    
    active_tickets = [t for t in st.session_state.tech_tickets if t['Status'] in ['In Progress', 'Approved']]
    
    if active_tickets:
        for ticket in active_tickets:
            with st.container(border=True):
                # Header
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{ticket['Title']}")
                    st.caption(f"**ID:** {ticket['Ticket ID']} | **User:** {ticket['User']}")
                with col2:
                    if ticket['Status'] == 'In Progress':
                        st.info(f"🔵 {ticket['Status']}", icon="🔵")
                    else:
                        st.success(f"✅ {ticket['Status']}", icon="✅")
                
                # Details in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("👤 Assigned To", ticket['Assigned Tech'] or 'Not assigned')
                with col2:
                    st.metric("📅 Collection Time", ticket['Collection Time'] or 'Not set')
                
                st.write(f"**Item:** {ticket['Requested Item']}")
                if ticket['Notes']:
                    st.write(f"**Notes:** {ticket['Notes']}")
                
                st.divider()
                
                # Quick Actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"✅ Mark Complete", key=f"complete_{ticket['Ticket ID']}", type="primary", use_container_width=True):
                        for t in st.session_state.tech_tickets:
                            if t['Ticket ID'] == ticket['Ticket ID']:
                                t['Status'] = 'Completed'
                        
                        st.success("✅ Completed!")
                        st.rerun()
                
                with col2:
                    if st.button(f"📝 Edit Details", key=f"edit_{ticket['Ticket ID']}", use_container_width=True):
                        st.info(f"Edit {ticket['Ticket ID']}")
    else:
        st.info("📭 No active tickets")

# ============= TAB 3: ALL TICKETS =============
with tab3:
    st.header("📊 All Tickets")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["Pending Approval", "Approved", "In Progress", "Completed", "Rejected"],
            default=["Pending Approval", "Approved", "In Progress"]
        )
    
    with col2:
        priority_filter = st.multiselect(
            "Filter by Priority",
            ["High", "Medium", "Low"],
            default=["High", "Medium", "Low"]
        )
    
    with col3:
        category_filter = st.multiselect(
            "Filter by Category",
            ["Hardware", "Software", "Network"],
            default=["Hardware", "Software", "Network"]
        )
    
    st.divider()
    
    # DataFrame
    df = pd.DataFrame(st.session_state.tech_tickets)
    
    # Apply filters
    filtered_df = df[
        (df['Status'].isin(status_filter)) &
        (df['Priority'].isin(priority_filter)) &
        (df['Category'].isin(category_filter))
    ]
    
    # Display table
    st.dataframe(
        filtered_df[['Ticket ID', 'User', 'Title', 'Status', 'Priority', 'Assigned Tech', 'Collection Time']],
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.divider()
    
    # Export
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📥 Export to CSV", use_container_width=True):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                f"tickets_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )

# ============= TAB 4: INVENTORY =============
with tab4:
    st.header("📦 Hardware Inventory")
    
    st.info("ℹ️ Inventory is managed in the backend database. Contact system admin to add or remove items.")
    
    # Get inventory from session state
    inventory_df = pd.DataFrame(st.session_state.inventory)
    
    st.dataframe(
        inventory_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Item": st.column_config.TextColumn("🔧 Item", width="medium"),
            "Total Stock": st.column_config.NumberColumn("📦 Total", width="small"),
            "Available": st.column_config.NumberColumn("✅ Available", width="small"),
            "Assigned": st.column_config.NumberColumn("📤 Assigned", width="small"),
            "In Repair": st.column_config.NumberColumn("🔨 Repair", width="small")
        },
        height=400
    )
    
    st.divider()
    
    # Low stock warnings
    st.subheader("⚠️ Low Stock Alerts")
    low_stock_items = inventory_df[inventory_df['Available'] < 20]
    
    if not low_stock_items.empty:
        for _, item in low_stock_items.iterrows():
            st.warning(f"🔴 **{item['Item']}**: Only {item['Available']} available")
    else:
        st.success("✅ All items have sufficient stock")
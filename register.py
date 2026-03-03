import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"   # ✅ Fixed: was localhost (inconsistent with login_frontend)

st.set_page_config(page_title="IT Support Help Desk", page_icon="🖥️", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1a1aff;'>🖥️ IT SUPPORT HELP DESK</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #5555cc;'>Register</h3>", unsafe_allow_html=True)
st.write("")

label_w, input_w = 2, 10

# Name
col1, col2 = st.columns([label_w, input_w], vertical_alignment="center")
with col1:
    st.write("**Name:**")
with col2:
    reg_name = st.text_input("reg_name", label_visibility="collapsed",
                             placeholder="Enter your full name")

# Email
col3, col4 = st.columns([label_w, input_w], vertical_alignment="center")
with col3:
    st.write("**Email:**")
with col4:
    reg_email = st.text_input("reg_email", label_visibility="collapsed",
                              placeholder="Enter your email")

# Password
col5, col6 = st.columns([label_w, input_w], vertical_alignment="center")
with col5:
    st.write("**Password:**")
with col6:
    reg_password = st.text_input("reg_password", type="password",
                                 label_visibility="collapsed",
                                 placeholder="Create a password (min 6 chars)")

# Confirm Password
col7, col8 = st.columns([label_w, input_w], vertical_alignment="center")
with col7:
    st.write("**Confirm:**")
with col8:
    reg_confirm = st.text_input("reg_confirm", type="password",
                                label_visibility="collapsed",
                                placeholder="Re-enter your password")

# Role ID
col9, col10 = st.columns([label_w, input_w], vertical_alignment="center")
with col9:
    st.write("**Role ID:**")
with col10:
    reg_role_id = st.number_input("reg_role_id", label_visibility="collapsed",
                                  min_value=1, step=1, value=1)

st.write("")
_, btn_col, _ = st.columns([2, 2, 2])
with btn_col:
    if st.button("Register", type="primary", use_container_width=True):
        if not all([reg_name, reg_email, reg_password, reg_confirm]):
            st.warning("⚠️ Please fill in all fields.")
        elif reg_password != reg_confirm:
            st.error("❌ Passwords do not match.")
        elif len(reg_password) < 6:
            st.warning("⚠️ Password must be at least 6 characters.")
        else:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/users/",
                    json={
                        "name": reg_name,
                        "email": reg_email,
                        "password": reg_password,
                        "role_id": int(reg_role_id)
                    }
                )
                if response.status_code == 201:                  # ✅ Fixed: backend now returns 201 for created
                    user_data = response.json()
                    st.success(f"✅ Account created for **{user_data['name']}**! You can now log in.")
                elif response.status_code == 400:
                    st.error("❌ An account with this email already exists.")
                else:
                    st.error(f"Unexpected error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to server. Make sure FastAPI is running on port 8000.")
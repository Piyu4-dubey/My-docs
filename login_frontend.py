import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="IT Support Help Desk", page_icon="🖥️", layout="centered")

st.markdown("<h1 style='text-align: center; color: #1a1aff;'>🖥️ IT SUPPORT HELP DESK</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #5555cc;'>Login</h3>", unsafe_allow_html=True)
st.write("")

label_w, input_w = 2, 10

# Email
col1, col2 = st.columns([label_w, input_w], vertical_alignment="center")
with col1:
    st.write("**Email:**")
with col2:
    user_email = st.text_input("login_email", label_visibility="collapsed",
                               placeholder="Enter your email")

# Password
col3, col4 = st.columns([label_w, input_w], vertical_alignment="center")
with col3:
    st.write("**Password:**")
with col4:
    password = st.text_input("login_password", type="password",
                             label_visibility="collapsed",
                             placeholder="Enter your password")

st.write("")
_, btn_col, _ = st.columns([2, 2, 2])
with btn_col:
    if st.button("Login", type="primary", use_container_width=True):
        if not user_email or not password:
            st.warning("⚠️ Please fill in both fields.")
        else:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/login/",
                    json={"email": user_email, "password": password}
                )
                if response.status_code == 200:
                    user_data = response.json()
                    st.session_state["user"] = user_data
                    st.success(f"✅ Welcome back, **{user_data['name']}**!")
                elif response.status_code == 401:
                    st.error("❌ Incorrect password.")
                elif response.status_code == 404:
                    st.error("❌ No account found with that email.")
                else:
                    st.error(f"Unexpected error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to server. Make sure FastAPI is running on port 8000.")

# Show session info if logged in
if "user" in st.session_state:
    u = st.session_state["user"]
    st.divider()
    st.info(f"🟢 Logged in as **{u['name']}** ({u['email']}) | Role ID: {u['role_id']}")
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()
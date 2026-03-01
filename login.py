import streamlit as st
# Main Heading
st.markdown("<h1 style='text-align: center; color: blue;'>IT SUPPORT HELP DESK</h1>", unsafe_allow_html=True)

# Sub Heading (Login)
st.markdown("<h2 style='text-align: center; color: blue;'>Login</h2>", unsafe_allow_html=True)





#st.title("Login Page")

#row col ratio
label_width = 2
input_width = 10

#input field
col1, col2 = st.columns([label_width, input_width], vertical_alignment="center")
with col1:
    st.write("**Name:**")
with col2:
    user_name = st.text_input("Name", label_visibility="collapsed", placeholder="Enter your name here")

 # Password Row
col_p1, col_p2 = st.columns([label_width, input_width], vertical_alignment="center")
with col_p1:
    st.write("**Password:**")
with col_p2:
    password = st.text_input("pass_input", type="password", label_visibility="collapsed",placeholder="Enter Password")

# Register button
# Create 3 columns; middle one holds the button
left_co, cent_co, last_co = st.columns([2, 2, 2], vertical_alignment="center")

with cent_co:
   
    if st.button("Login", type="primary", use_container_width=True):
        # Ensure user_name is defined 
        st.success(f"Welcome {user_name}!")
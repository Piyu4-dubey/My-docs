import streamlit as st

st.title("Registration Page")

# row col ratio
label_width = 1
input_width = 10

# Name field
col1, col2 = st.columns([label_width, input_width], vertical_alignment="center")
with col1:
    st.write("**Name:**")
with col2:
    user_name = st.text_input("Name", label_visibility="collapsed", placeholder="Enter your name here")

# Role field
col1, col2 = st.columns([label_width, input_width], vertical_alignment="center")
with col1:
    st.write("**Role:**")
with col2:
    # Added label_visibility="collapsed" here to match alignment
    user_pos = st.selectbox("Role", ("Intern","Trainee","Associate","HR","Manager","Team Lead"), label_visibility="collapsed")

#employee id


label_w = 1
input_w = 4 # Adjusting from 20 to 4 for better spacing

has_emp_id = st.radio("Do you have an Emp. Id?", ("Yes", "No"))

if has_emp_id == "Yes":
    col1, col2 = st.columns([label_w, input_w], vertical_alignment="center")
    with col1:
        st.write("**Employee ID:**")
    with col2:
        emp_id = st.text_input("emp_id_input", label_visibility="collapsed", placeholder="Enter Emp. Id")

else:
    # Email Row
    col_e1, col_e2 = st.columns([label_w, input_w], vertical_alignment="center")
    with col_e1:
        st.write("**Email:**")
    with col_e2:
        email = st.text_input("email_input", label_visibility="collapsed")
    
    # Password Row
    col_p1, col_p2 = st.columns([label_w, input_w], vertical_alignment="center")
    with col_p1:
        st.write("**Password:**")
    with col_p2:
        password = st.text_input("pass_input", type="password", label_visibility="collapsed")


# Register button
# Create 3 columns; middle one holds the button
left_co, cent_co, last_co = st.columns([2, 2, 2])

with cent_co:
    if st.button("Register"):
        st.success("Registered Successfully!")


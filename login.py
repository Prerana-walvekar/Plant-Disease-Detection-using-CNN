import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

API_KEY = "AIzaSyBMM5yD7mYiqHv4oXCsBq_hfj_VA7WpIGs"

FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
FIREBASE_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={API_KEY}"

st.set_page_config(page_title="Plant Disease Detection", layout="centered")
st.title(':green[Plant Disease Detection]')

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

choice = st.selectbox("Login/Signup", ["Login", "Sign Up"])

def login_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    res = requests.post(FIREBASE_SIGNIN_URL, json=payload)
    return res

def create_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    res = requests.post(FIREBASE_SIGNUP_URL, json=payload)
    return res

def send_password_reset(email):
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    res = requests.post(FIREBASE_RESET_URL, json=payload)
    return res

# Login Section
if choice == "Login":
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            result = login_user(email, password)
            if result.status_code == 200:
                st.success("Login successful!")
                st.session_state.authenticated = True
                st.session_state.email = email  # store user email if needed
                switch_page("main2")
            else:
                st.session_state.authenticated = False
                error_msg = result.json().get("error", {}).get("message", "Login failed.")
                st.error(f"Error: {error_msg}")
        else:
            st.warning("Please fill in both fields.")

    with st.expander("Forgot Password?"):
        reset_email = st.text_input("Enter your registered email")
        if st.button("Send Reset Link"):
            if reset_email:
                response = send_password_reset(reset_email)
                if response.status_code == 200:
                    st.success("Password reset email sent!")
                else:
                    st.error("Failed to send reset email.")
            else:
                st.warning("Please enter an email address.")

# Signup Section
else:
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not email or not password or not confirm_password:
            st.warning("All fields are required.")
        elif password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            result = create_user(email, password)
            if result.status_code == 200:
                st.success("Account created successfully! Please login.")
            else:
                error_msg = result.json().get("error", {}).get("message", "Signup failed.")
                st.error(f"Error: {error_msg}")

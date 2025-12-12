# app.py
import streamlit as st
from components.auth import auth_router
from components.job_seeker import job_seeker_ui
from components.employer import employer_ui
from components.admin import admin_ui
from database import init_db

st.set_page_config(page_title="Job Portal", layout="wide")
init_db()  # harmless if already initialized

st.markdown("<h1 style='text-align:center;'>💼 Job Portal</h1>", unsafe_allow_html=True)

if "user" not in st.session_state:
    auth_router()
else:
    role = st.session_state.get("type")
    user = st.session_state.get("user")
    if role == "job_seeker":
        job_seeker_ui(user)
    elif role == "employer":
        employer_ui(user)
    elif role == "admin":
        admin_ui(user)
    else:
        st.error("Unknown role. Please log in again.")
        if st.button("Logout"):
            st.session_state.pop("user", None)
            st.session_state.pop("type", None)
            st.experimental_rerun()

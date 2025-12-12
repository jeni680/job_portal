# components/auth.py
import streamlit as st
import bcrypt
from database import get_connection

# ---------------- Helpers ---------------- #
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def check_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

# ---------------- REGISTER UI ---------------- #
def register_ui():
    st.title("📝 Create a New Account")
    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Account Type", ["Job Seeker", "Employer"])
        submit = st.form_submit_button("Register")

    if submit:
        # Validation
        if not username or not password:
            st.error("Username and password required.")
            return
        if len(password) < 4:
            st.error("Password must be at least 4 characters.")
            return

        conn = get_connection()
        cur = conn.cursor()
        # Check duplicate first (case-insensitive)
        cur.execute("SELECT 1 FROM users WHERE LOWER(username) = LOWER(?);", (username,))
        if cur.fetchone():
            conn.close()
            st.error("Username already exists. Pick another.")
            return  # EARLY RETURN - prevents double messages

        try:
            cur.execute(
                "INSERT INTO users (username, password, type) VALUES (?, ?, ?);",
                (username, hash_password(password), "job_seeker" if role == "Job Seeker" else "employer")
            )
            conn.commit()
            conn.close()
            st.success("✅ Registration successful — you are now logged in.")
            # Auto-login the new user
            st.session_state["user"] = username
            st.session_state["type"] = "job_seeker" if role == "Job Seeker" else "employer"
            st.rerun()
        except Exception:
            conn.close()
            st.error("Could not create account. Try another username.")

# ---------------- UNIFIED LOGIN UI ---------------- #
def login_ui():
    st.title("💼 Job Searching Assistant – Login")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if not username or not password:
            st.error("Enter username and password.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password, type FROM users WHERE username = ?;", (username,))
        row = cur.fetchone()
        conn.close()

        if not row:
            st.error("Invalid username or password.")
            return

        if not check_password(password, row["password"]):
            st.error("Invalid username or password.")
            return

        # At this point, credentials are valid. Set session and redirect based on role.
        st.session_state["user"] = username
        st.session_state["type"] = row["type"]
        st.rerun()

# ---------------- AUTH ROUTER ---------------- #
def auth_router():
    tabs = st.tabs(["🔑 Login", "📝 Register"])
    with tabs[0]:
        login_ui()
    with tabs[1]:
        register_ui()

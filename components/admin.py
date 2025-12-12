# components/admin.py
import streamlit as st
import uuid
from database import get_connection, init_db

def admin_ui(username):
    st.subheader(f"🔒 Admin Panel — Logged in as **{username} (Admin)**")
    if st.button("Log out"):
        st.session_state.pop("user", None)
        st.session_state.pop("type", None)
        st.rerun()

    tabs = st.tabs(["👥 Users", "📋 Jobs", "📨 Applications", "⚙️ Utilities"])

    # ------------------ Users ------------------
    with tabs[0]:
        st.markdown("### All Users")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, type, created_at FROM users ORDER BY created_at DESC;")
        users = cur.fetchall()
        if not users:
            st.info("No users.")
        else:
            for u in users:
                st.write(f"- **{u['username']}** ({u['type']}) — created at {u['created_at']}")

        st.markdown("### Add New User (Admin tool)")
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["job_seeker", "employer", "admin"])
            add_submit = st.form_submit_button("Add User")
        if add_submit:
            if not new_username or not new_password:
                st.error("Provide username and password.")
            else:
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    # hash with bcrypt
                    import bcrypt
                    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                    cur.execute("INSERT INTO users (username, password, type) VALUES (?, ?, ?);",
                                (new_username, hashed, new_role))
                    conn.commit()
                    conn.close()
                    st.success("User created.")
                    st.rerun()
                except Exception:
                    st.error("Could not create user (maybe username exists).")

        st.markdown("### Delete a User")
        with st.form("delete_user_form"):
            del_username = st.text_input("Username to delete")
            del_submit = st.form_submit_button("Delete User")
        if del_submit:
            if not del_username:
                st.error("Provide username.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT username FROM users WHERE username = ?;", (del_username,))
                if not cur.fetchone():
                    st.error("User not found.")
                    conn.close()
                else:
                    cur.execute("DELETE FROM users WHERE username = ?;", (del_username,))
                    conn.commit()
                    conn.close()
                    st.success("User deleted (cascade removed their jobs/applications).")
                    st.rerun()

    # ------------------ Jobs ------------------
    with tabs[1]:
        st.markdown("### All Jobs")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs ORDER BY created_at DESC;")
        jobs = cur.fetchall()
        conn.close()
        if not jobs:
            st.info("No jobs.")
        else:
            for j in jobs:
                st.write(f"- **{j['title']}** — {j['company']} (ID: {j['id']}) — posted by `{j['employer']}` at {j['created_at']}")
        st.markdown("### Delete a Job")
        with st.form("del_job_form"):
            del_job_id = st.text_input("Job ID to delete")
            del_job_submit = st.form_submit_button("Delete Job")
        if del_job_submit:
            if not del_job_id:
                st.error("Provide Job ID.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT id FROM jobs WHERE id = ?;", (del_job_id,))
                if not cur.fetchone():
                    st.error("Job not found.")
                    conn.close()
                else:
                    cur.execute("DELETE FROM jobs WHERE id = ?;", (del_job_id,))
                    conn.commit()
                    conn.close()
                    st.success("Job deleted (applications removed).")
                    st.rerun()

    # ------------------ Applications ------------------
    with tabs[2]:
        st.markdown("### All Applications")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, a.username, a.job_id, j.title, j.company, a.applied_at
            FROM applications a
            LEFT JOIN jobs j ON a.job_id = j.id
            ORDER BY a.applied_at DESC;
        """)
        apps = cur.fetchall()
        conn.close()
        if not apps:
            st.info("No applications.")
        else:
            for a in apps:
                st.write(f"- **{a['username']}** applied to **{a['title'] or 'Unknown Job'}** ({a['company'] or 'Unknown'}) — {a['applied_at']}")

    # ------------------ Utilities: Seed & Reset ------------------
    with tabs[3]:
        st.markdown("### Seed Database (adds sample users, employers, jobs, applications)")
        if st.button("Run Seed (Add sample data)"):
            run_seed()
            st.success("Seeding done.")
            st.rerun()

        st.markdown("### Factory Reset (DROP & Recreate tables)")
        st.warning("This will erase ALL data permanently.")
        if st.button("Factory Reset Database"):
            run_reset()
            st.success("Database reset.")
            st.rerun()
# ---------- seed & reset helpers ----------
def run_seed():
    conn = get_connection()
    cur = conn.cursor()
    # sample users (3 employers, 5 job seekers, 1 admin)
    import bcrypt
    sample_users = [
        ("employerA", bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode(), "employer"),
        ("employerB", bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode(), "employer"),
        ("employerC", bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode(), "employer"),
        ("seeker1", bcrypt.hashpw("pass1".encode(), bcrypt.gensalt()).decode(), "job_seeker"),
        ("seeker2", bcrypt.hashpw("pass2".encode(), bcrypt.gensalt()).decode(), "job_seeker"),
        ("seeker3", bcrypt.hashpw("pass3".encode(), bcrypt.gensalt()).decode(), "job_seeker"),
        ("seeker4", bcrypt.hashpw("pass4".encode(), bcrypt.gensalt()).decode(), "job_seeker"),
        ("seeker5", bcrypt.hashpw("pass5".encode(), bcrypt.gensalt()).decode(), "job_seeker"),
        ("admin", bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(), "admin"),
    ]
    for u in sample_users:
        try:
            cur.execute("INSERT INTO users (username, password, type) VALUES (?, ?, ?);", u)
        except:
            pass

    # sample jobs (10)
    import uuid
    sample_jobs = [
        (uuid.uuid4().hex, "Backend Developer", "employerA", "Work on APIs", "Kochi", "₹40,000"),
        (uuid.uuid4().hex, "Frontend Developer", "employerB", "React apps", "Kochi", "₹35,000"),
        (uuid.uuid4().hex, "Data Analyst", "employerA", "SQL and viz", "Kottayam", "₹30,000"),
        (uuid.uuid4().hex, "DevOps Engineer", "employerC", "CI/CD & infra", "Bengaluru", "₹70,000"),
        (uuid.uuid4().hex, "Mobile Developer", "employerB", "Flutter apps", "Kochi", "₹45,000"),
        (uuid.uuid4().hex, "QA Engineer", "employerA", "Testing & automation", "Kollam", "₹28,000"),
        (uuid.uuid4().hex, "Fullstack Engineer", "employerC", "End-to-end", "Kochi", "₹55,000"),
        (uuid.uuid4().hex, "ML Engineer", "employerA", "Models & pipelines", "Trivandrum", "₹90,000"),
        (uuid.uuid4().hex, "Product Manager", "employerB", "Leading product", "Kochi", "₹85,000"),
        (uuid.uuid4().hex, "Support Engineer", "employerC", "Customer support", "Kottayam", "₹25,000"),
    ]
    for job in sample_jobs:
        try:
            cur.execute("INSERT INTO jobs (id, title, company, description, location, salary, employer) VALUES (?, ?, ?, ?, ?, ?, ?);",
                        (job[0], job[1], job[2], job[3], job[4], job[5], job[2]))
        except:
            pass

    # sample applications (15) — distribute among seekers & jobs
    cur.execute("SELECT id FROM jobs;")
    job_ids = [r["id"] for r in cur.fetchall()]
    sample_apps = []
    seekers = ["seeker1","seeker2","seeker3","seeker4","seeker5"]
    import random
    for _ in range(15):
        sample_apps.append((random.choice(seekers), random.choice(job_ids)))
    for a in sample_apps:
        try:
            cur.execute("INSERT INTO applications (username, job_id) VALUES (?, ?);", a)
        except:
            pass

    conn.commit()
    conn.close()

def run_reset():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS applications;")
    cur.execute("DROP TABLE IF EXISTS jobs;")
    cur.execute("DROP TABLE IF EXISTS users;")
    conn.commit()
    conn.close()
    # recreate
    init_db()

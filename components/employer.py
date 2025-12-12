# components/employer.py
import streamlit as st
import uuid
from database import get_connection

def employer_ui(username):
    st.subheader(f"Logged in as **{username} (Employer)**")
    if st.button("Log out"):
        st.session_state.pop("user", None)
        st.session_state.pop("type", None)
        st.rerun()


    tab1, tab2 = st.tabs(["➕ Add Job", "📌 My Job Listings"])

    # Add Job
    with tab1:
        with st.form("add_job_form"):
            title = st.text_input("Job Title")
            company = st.text_input("Company", value=username)
            description = st.text_area("Job Description")
            location = st.text_input("Location")
            salary = st.text_input("Salary")
            submit = st.form_submit_button("Submit Job")

        if submit:
            if not title or not company:
                st.error("Title and company required.")
            else:
                conn = get_connection()
                cur = conn.cursor()
                job_id = uuid.uuid4().hex
                cur.execute("""
                    INSERT INTO jobs (id, title, company, description, location, salary, employer)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (job_id, title, company, description, location, salary, username))
                conn.commit()
                conn.close()
                st.success("Job posted successfully.")

    # My Job Listings
    with tab2:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE employer = ? ORDER BY created_at DESC;", (username,))
        jobs = cur.fetchall()
        conn.close()

        if not jobs:
            st.info("No job postings yet.")
        else:
            for job in jobs:
                job_id = job["id"]
                with st.expander(f"{job['title']} — {job['company']}  (ID: {job_id})"):
                    st.markdown(f"**Location:** {job['location']}  |  **Salary:** {job['salary']}")
                    st.write(job["description"])

                    col1, col2, col3 = st.columns([1,1,1])
                    with col1:
                        if st.button("Edit", key=f"edit_{job_id}"):
                            st.session_state["edit_job_id"] = job_id
                            st.rerun()
                    with col2:
                        if st.button("View Applicants", key=f"view_{job_id}"):
                            st.session_state["view_app_job_id"] = job_id
                            st.rerun()
                    with col3:
                        if st.button("Delete", key=f"del_{job_id}"):
                            conn = get_connection()
                            cur = conn.cursor()
                            cur.execute("DELETE FROM jobs WHERE id = ? AND employer = ?;", (job_id, username))
                            conn.commit()
                            conn.close()
                            st.success("Job deleted.")
                            st.rerun()

    # Edit Job Modal
    if "edit_job_id" in st.session_state:
        edit_id = st.session_state["edit_job_id"]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE id = ? AND employer = ?;", (edit_id, username))
        job = cur.fetchone()
        conn.close()
        if not job:
            st.error("Job not found or permission denied.")
            st.session_state.pop("edit_job_id", None)
        else:
            st.markdown("### Edit Job")
            with st.form("edit_job_form"):
                new_title = st.text_input("Job Title", value=job["title"])
                new_company = st.text_input("Company", value=job["company"])
                new_description = st.text_area("Job Description", value=job["description"])
                new_location = st.text_input("Location", value=job["location"])
                new_salary = st.text_input("Salary", value=job["salary"])
                save = st.form_submit_button("Save Changes")
            if save:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    UPDATE jobs
                    SET title=?, company=?, description=?, location=?, salary=?
                    WHERE id=? AND employer=?;
                """, (new_title, new_company, new_description, new_location, new_salary, edit_id, username))
                conn.commit()
                conn.close()
                st.success("Job updated.")
                st.session_state.pop("edit_job_id", None)
                st.rerun()

    # View Applicants Modal (employer)
    if "view_app_job_id" in st.session_state:
        vid = st.session_state["view_app_job_id"]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs WHERE id = ? AND employer = ?;", (vid, username))
        job = cur.fetchone()
        if not job:
            st.error("Job not found or access denied.")
            conn.close()
            st.session_state.pop("view_app_job_id", None)
            st.rerun()
        else:
            st.markdown(f"### Applicants for {job['title']}")
            cur.execute("""
                SELECT a.username, a.applied_at
                FROM applications a
                WHERE a.job_id = ?
                ORDER BY a.applied_at DESC;
            """, (vid,))
            apps = cur.fetchall()
            conn.close()
            if not apps:
                st.info("No applicants yet.")
            else:
                for a in apps:
                    st.write(f"- **{a['username']}** applied at {a['applied_at']}")
            if st.button("Close Applicants"):
                st.session_state.pop("view_app_job_id", None)
                st.rerun()

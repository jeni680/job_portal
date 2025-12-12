# components/job_seeker.py
import streamlit as st
from database import get_connection

def job_seeker_ui(username):
    st.subheader(f"Logged in as **{username} (Job Seeker)**")
    if st.button("Log out"):
        st.session_state.pop("user", None)
        st.session_state.pop("type", None)
        st.rerun()

    tab1, tab2 = st.tabs(["🔍 Available Jobs", "📄 Your Applications"])

    # Available Jobs - search & filters
    with tab1:
        with st.form("search_form", clear_on_submit=False):
            search = st.text_input("Search (title/company/description):")
            location = st.text_input("Filter by location (optional):")
            salary = st.text_input("Filter by salary substring (optional):")
            submit = st.form_submit_button("Search")
        # Build SQL
        sql = "SELECT * FROM jobs"
        params = []
        where = []
        if search:
            where.append("(title LIKE ? OR company LIKE ? OR description LIKE ?)")
            s = f"%{search}%"
            params.extend([s,s,s])
        if location:
            where.append("location LIKE ?")
            params.append(f"%{location}%")
        if salary:
            where.append("salary LIKE ?")
            params.append(f"%{salary}%")
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY created_at DESC LIMIT 200;"

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        jobs = cur.fetchall()

        # user's applied jobs
        cur.execute("SELECT job_id FROM applications WHERE username = ?;", (username,))
        applied_rows = cur.fetchall()
        applied_set = {r["job_id"] for r in applied_rows}
        conn.close()

        if not jobs:
            st.info("No jobs found.")
        else:
            for job in jobs:
                jid = job["id"]
                with st.container():
                    st.markdown(f"### {job['title']} — {job['company']}")
                    st.write(job["description"])
                    st.write(f"📍 {job['location']}  |  💰 {job['salary']}  |  `ID: {jid}`")
                    if jid in applied_set:
                        st.success("✅ Already Applied")
                    else:
                        if st.button("Apply", key=f"apply_{jid}"):
                            try:
                                conn = get_connection()
                                cur = conn.cursor()
                                cur.execute("INSERT INTO applications (username, job_id) VALUES (?, ?);", (username, jid))
                                conn.commit()
                                conn.close()
                                st.success("Applied successfully!")
                                st.rerun()
                            except Exception:
                                st.error("Could not apply (maybe already applied).")

    # Your Applications
    with tab2:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.applied_at, j.id as job_id, j.title, j.company, j.location, j.salary
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.username = ?
            ORDER BY a.applied_at DESC;
        """, (username,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            st.info("You haven't applied to any jobs yet.")
        else:
            for r in rows:
                st.markdown(f"### {r['title']} — {r['company']}")
                st.write(f"📍 {r['location']}  |  💰 {r['salary']}  |  Applied at: {r['applied_at']}")
                st.write(f"Job ID: `{r['job_id']}`")

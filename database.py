# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path("job_portal.db")

def get_connection():
    # check_same_thread=False so Streamlit (multi-threaded) doesn't choke
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # enforce foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('job_seeker','employer','admin')),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # jobs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        description TEXT,
        location TEXT,
        salary TEXT,
        employer TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employer) REFERENCES users(username) ON DELETE CASCADE
    );
    """)

    # applications - unique constraint prevents duplicate apps
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        job_id TEXT NOT NULL,
        applied_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        UNIQUE(username, job_id)
    );
    """)

    conn.commit()
    conn.close()

# initialize on import
init_db()

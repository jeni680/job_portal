import sqlite3
import bcrypt

DB = "job_portal.db"

employers = [
    "Infosys",
    "Wipro",
    "Accenture",
    "Cognizant",
    "IBM",
    "UST Global",
    "Oracle",
    "Capgemini",
    "Zoho",
]

hashed_pw = bcrypt.hashpw("1234".encode(), bcrypt.gensalt()).decode()

conn = sqlite3.connect(DB)
cur = conn.cursor()

for company in employers:
    try:
        cur.execute(
            "INSERT INTO users (username, password, type) VALUES (?, ?, ?)",
            (company, hashed_pw, "employer")
        )
        print(f"✅ Added employer: {company}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Skipped (already exists): {company}")

conn.commit()
conn.close()

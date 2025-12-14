import sqlite3
import uuid
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "job_portal.db")

jobs = [
    # employer, title, company, description, location, salary
    ("Infosys", "Python Backend Developer", "Infosys", "FastAPI + PostgreSQL APIs", "Bangalore", "₹50,000"),
    ("Infosys", "System Engineer", "Infosys", "Enterprise software maintenance", "Mysore", "₹35,000"),

    ("Wipro", "Java Developer", "Wipro", "Spring Boot microservices", "Chennai", "₹45,000"),
    ("Wipro", "QA Engineer", "Wipro", "Automation & manual testing", "Kochi", "₹30,000"),

    ("Accenture", "Data Analyst", "Accenture", "SQL + Power BI dashboards", "Hyderabad", "₹55,000"),
    ("Accenture", "Cloud Engineer", "Accenture", "AWS infrastructure", "Pune", "₹65,000"),

    ("Cognizant", "Full Stack Developer", "Cognizant", "React + Node.js", "Kochi", "₹60,000"),
    ("IBM", "ML Engineer", "IBM", "Model training & deployment", "Bangalore", "₹90,000"),

    ("Zoho", "Product Engineer", "Zoho", "Core product development", "Chennai", "₹70,000"),
    ("Oracle", "Database Engineer", "Oracle", "Oracle DB optimization", "Hyderabad", "₹80,000"),
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

for employer, title, company, desc, location, salary in jobs:
    cur.execute(
        """
        INSERT INTO jobs (id, title, company, description, location, salary, employer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (str(uuid.uuid4()), title, company, desc, location, salary, employer)
    )
    print(f"✅ Added: {title} @ {company}")

conn.commit()
conn.close()

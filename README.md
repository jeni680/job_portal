# 💼 Job Portal – Role-Based Job Management System

A full-stack **role-based Job Portal application** built using **Python, Streamlit, and SQLite**, designed to simulate a real-world recruitment platform with **Admin, Employer, and Job Seeker** roles.

This project goes beyond a basic CRUD demo and focuses on **clean architecture, data integrity, role-based access control, and realistic workflows**, making it suitable for **interviews, academic projects, and demos**.

---

## 🚀 Features Overview

### 👤 Authentication & Security

* Secure user authentication
* Password hashing using **bcrypt**
* Role-based routing after login
* Session-based access control

### 🧑‍💼 Roles & Capabilities

#### 🔑 Admin

* View all users (admins, employers, job seekers)
* View all job postings
* View all applications
* Seed database with sample users and jobs (for demo purposes)

#### 🏢 Employer

* Create job postings
* Edit and delete own jobs
* View only jobs posted by the employer

#### 🎓 Job Seeker

* Browse available jobs
* Search & filter jobs
* Apply to jobs
* Prevent duplicate applications
* View applied jobs

---

## 🧱 Tech Stack

| Layer    | Technology  |
| -------- | ----------- |
| Language | Python 3.13 |
| Frontend | Streamlit   |
| Database | SQLite      |
| Security | bcrypt      |
| IDs      | UUID        |

---

## 📁 Project Structure

```text
job_portal/
│
├── app.py
├── job_portal.db
│
├── components/
│   ├── auth.py        # Login & registration logic
│   ├── admin.py       # Admin dashboard
│   ├── employer.py    # Employer dashboard
│   └── job_seeker.py  # Job seeker dashboard
│
├── seed_employers.py  # Bulk employer creation
├── seed_jobs.py       # Bulk job creation
└── README.md
```

---

## 🗄️ Database Design

### users

* username (PRIMARY KEY)
* password (bcrypt hashed)
* type (admin / employer / job_seeker)
* created_at

### jobs

* id (UUID PRIMARY KEY)
* title
* company
* description
* location
* salary
* employer (foreign key reference)
* created_at

### applications

* id
* username
* job_id
* applied_at

---

## ⚙️ How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install streamlit bcrypt
```

### 2️⃣ Run the app

```bash
streamlit run app.py
```

### 3️⃣ Access in browser

```
http://localhost:8501
```

---

## 🔐 Demo Credentials

### Admin

* **Username:** admin
* **Password:** admin123

### Employers (password same for all)

* Infosys / Wipro / Accenture / IBM / Zoho
* **Password:** 1234

### Job Seeker

* Register a new account via UI

---

## 📊 Sample Data

The project supports **bulk seeding** using Python scripts:

* `seed_employers.py` → Adds multiple employers
* `seed_jobs.py` → Adds multiple jobs linked to employers

This makes the app **demo-ready instantly**.

---

## 🎯 Why This Project Stands Out

* Role-based architecture (not just CRUD)
* Secure password handling
* Clean separation of concerns
* Proper database constraints
* Realistic data flow
* Interview-ready complexity

---

## 🧠 Future Enhancements (Optional)

* Analytics dashboard for admin
* Resume upload for job seekers
* Email notifications
* Pagination & advanced search

---

## 📌 Note

This project is intended for **learning, demonstration, and academic purposes**. Shared passwords are used **only for demo convenience**.

---


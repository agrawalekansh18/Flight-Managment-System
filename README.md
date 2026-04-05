# ✈️ Air Ticket Management System (ATMS)

A **console-based Air Ticket Management System** built using **Python and MySQL**, supporting both **user** and **admin** workflows. The system enables flight browsing, booking, cancellation, and administrative control over flights and users.

---

## 📌 Features

### 👤 User Functionalities
- Create account and login
- View all available flights
- Search flights by route (departure & arrival)
- Book flight tickets
- View booking details
- Cancel bookings
- Update account details (password, email, phone)

### 🛠️ Admin Functionalities
- View all flights
- Add new flights
- Modify flight details
- Remove flights
- View all bookings
- Cancel customer bookings
- View registered users
- Remove users
- Change admin password

---

## 🗂️ Project Structure

```
.
├── Main code.py
├── db_utils.py
├── schema.py
├── globalobjects.py
├── db_config.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Requirements

- Python 3.x
- MySQL Server
- mysql-connector-python

```bash
pip install mysql-connector-python
```

---

### 2️⃣ Configure Database

Create `db_config.py`:

```python
config = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password"
}
```

---

### 3️⃣ Run the Application

```bash
python "Main code.py"
```

---

## 🧠 Architecture Overview

### 🔹 Database Layer
- Centralized query execution
- Automatic commit/rollback
- User-friendly error handling

### 🔹 Schema Design
- Flights: unique composite constraint
- Users: unique email & phone
- Bookings: foreign keys with cascade delete
- Admins: separate authentication

### 🔹 Global Connection Handling
- Shared connection and cursor

---

## 🔐 Data Integrity & Validation

### ✅ Database-Level
- Primary keys, foreign keys
- Unique constraints
- CHECK constraints
- Cascading deletes

### ⚠️ Application-Level
- Input validation loops
- Duplicate checks
- Existence verification

---

## ⚡ Error Handling

Common database errors are mapped to readable messages:
- Duplicate entry
- Invalid references
- Dependency violations
- Missing required fields

---

## ▶️ Usage Flow

### Login
- User/Admin selection
- Signup/Login

### Menu System
- Loop-driven CLI using match-case

### Booking Flow
1. Select flight
2. Enter date & tickets
3. Confirm booking
4. Receive Booking ID

---

## ⚠️ Limitations

- Console-based (no GUI)
- Plain-text passwords
- Tight coupling of logic and UI

---

## 🚀 Future Improvements

- Password hashing (bcrypt)
- Logging system
- GUI/Web interface
- Layered architecture
- Added functionalities 
- ORM integration

---

## 📖 Key Files

- Main code.py: Application flow
- db_utils.py: DB utilities
- schema.py: DB schema
- globalobjects.py: DB connection

---
## 📌 Summary

This project demonstrates:
- Strong database integrity usage
- Structured CLI design
- Modular database handling

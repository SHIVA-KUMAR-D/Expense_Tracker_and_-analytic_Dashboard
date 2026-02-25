# 💰 FinSight — Smart Expense Tracker

*A Full-Stack Expense Management Web App (Flask + SQLite)*

## 📌 Overview

**FinSight** is a lightweight full-stack web application that helps users track, manage, and visualize their daily expenses.
It includes secure authentication, user-specific data storage, and an interactive dashboard with analytics.

The project demonstrates core backend development concepts using **Flask**, database management with **SQLite**, and frontend interactivity using **HTML, CSS, JavaScript, and Chart.js**.

---

## ✨ Key Features

### 🔐 Authentication

* User registration with unique usernames
* Secure login system
* Password hashing (Werkzeug)
* Session-based authentication
* Logout functionality

### 💸 Expense Management

* Add new expenses with category and date
* Delete expenses
* User-specific expense data (multi-user support)
* Real-time updates without page reload

### 📊 Analytics Dashboard

* Total expense calculation
* Category-wise spending visualization
* Interactive pie chart (Chart.js)

### 🗄️ Database

* SQLite local database
* Separate tables for users and expenses
* Automatic database initialization

---

## 🏗️ Tech Stack

### Backend

* Python 3.x
* Flask
* SQLite3
* Werkzeug Security

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Chart.js

---

## 📁 Project Structure

```
FinSight/
│
├── app.py          # Main Flask application
├── expenses.db     # SQLite database (auto-created)
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd FinSight
```

### 2️⃣ Install Dependencies

```bash
pip install flask werkzeug
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

### Authentication Flow

1. User registers → credentials stored in database
2. Password stored as hashed value
3. User logs in → session created
4. Protected routes require active session
5. Logout clears session

---

### Expense Flow

1. Logged-in user adds expense
2. Expense saved with user ID
3. Dashboard fetches only that user's data
4. Chart updates dynamically

---

## 🗃️ Database Schema

### Users Table

| Field    | Type    | Description     |
| -------- | ------- | --------------- |
| id       | INTEGER | Primary key     |
| username | TEXT    | Unique username |
| password | TEXT    | Hashed password |

---

### Expenses Table

| Field    | Type    | Description      |
| -------- | ------- | ---------------- |
| id       | INTEGER | Primary key      |
| user_id  | INTEGER | Linked user      |
| title    | TEXT    | Expense title    |
| amount   | REAL    | Expense amount   |
| category | TEXT    | Expense category |
| date     | TEXT    | Expense date     |

---

## 🔒 Security Features

* Password hashing using Werkzeug
* Session management
* User-level data isolation
* Protection of sensitive routes

---

## 🚀 Future Enhancements

* Monthly budgets and alerts
* Expense editing functionality
* Export to CSV/PDF
* Mobile-responsive UI
* Email-based authentication
* REST API support
* Deployment on cloud platforms
* Integration with payment apps

---

## 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Full-stack web development
* RESTful route design
* Database integration
* Authentication systems
* Client-server interaction
* Data visualization

---

## 👨‍💻 Author

**Shiva Kumar**
B.Tech CSE Student

---

## 📄 License

This project is for educational purposes.
Feel free to use and modify for learning or academic submissions.

---

## ⭐ Acknowledgements

* Flask Documentation
* SQLite Documentation
* Chart.js Library

---

## 📬 Contact

For suggestions or improvements, feel free to connect.(cseasriindu0539@gmail.com)

---

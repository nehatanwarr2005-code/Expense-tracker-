# 💰 Expense Tracker Web Application

A full-stack personal finance web application built using **Python (Flask)**, **SQLite**, and **vanilla JavaScript**. It allows users to record daily expenditures, categorize spending, and view aggregated financial summaries.

---

## 🚀 Features

- **Expense Management (CRUD)**: Log new expenses with title, amount, category, and date. View and delete entries in real time.
- **Category-wise Summary**: Aggregates expenditures by category using SQL `GROUP BY` and computes percentages of total spend.
- **Input Validation**: Server-side checks for numeric amounts, positive values, string limits, and ISO date compliance (`YYYY-MM-DD`).
- **SQL Injection Prevention**: Built entirely with parameterized queries (`?` placeholders).
- **Lightweight Single Page Frontend**: Dynamic interface powered by vanilla JavaScript and the modern `fetch()` API without bulky frontend frameworks.

---

## 🛠️ Tech Stack & Skills

- **Backend**: Python 3, Flask
- **Database**: SQLite (SQL queries with `GROUP BY`, `SUM`, parameterized statements)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+ Fetch API, DOM manipulation)
- **API Architecture**: RESTful API design

---

## 📡 REST API Documentation

| Method | Endpoint | Description | Request Body / Parameters | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Web user interface | None | `200 OK` |
| `GET` | `/api/expenses` | List all logged expenses | None | `200 OK` |
| `POST` | `/api/expenses` | Create a new expense | JSON: `{ "title": "...", "amount": 12.50, "category": "...", "spent_on": "2026-10-12" }` | `201 Created`, `400 Bad Request` |
| `DELETE` | `/api/expenses/<id>` | Remove an expense by ID | URL path param: `id` | `204 No Content`, `404 Not Found` |
| `GET` | `/api/summary` | Spending grouped by category | None | `200 OK` |

---

## 📂 Project Structure

```text
expense-tracker/
├── app.py                 # Flask server, route definitions, DB queries
├── requirements.txt       # Project dependencies
├── .gitignore             # Excludes database and virtual environment
├── README.md              # Project documentation and API specs
├── templates/
│   └── index.html         # Web dashboard template
└── static/
    ├── css/
    │   └── style.css      # Custom responsive styling
    └── js/
        └── app.js         # Fetch API client and DOM logic
```

---

## ⚙️ Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
```

### 2. Set up a virtual environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```
*(The SQLite database `expenses.db` and required tables will be created automatically on first run).*

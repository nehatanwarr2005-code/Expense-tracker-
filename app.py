"""Expense Tracker - Flask backend with SQLite database."""
import os
import sqlite3
from datetime import datetime
from flask import Flask, g, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "expenses.db")

app = Flask(__name__)


def get_db():
    """Open one database connection per request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    """Close the database connection when request context ends."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize database tables."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL,
                spent_on TEXT NOT NULL
            )"""
        )


@app.route("/")
def index():
    """Serve the main frontend user interface."""
    return render_template("index.html")


@app.route("/api/expenses", methods=["GET"])
def list_expenses():
    """Fetch all expenses sorted chronologically (newest first)."""
    rows = get_db().execute(
        "SELECT id, title, amount, category, spent_on FROM expenses "
        "ORDER BY spent_on DESC, id DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200


@app.route("/api/expenses", methods=["POST"])
def add_expense():
    """Create a new expense entry with input validation."""
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    category = (data.get("category") or "").strip()
    spent_on = (data.get("spent_on") or "").strip()
    raw_amount = data.get("amount")

    # Validate amount
    try:
        amount = round(float(raw_amount), 2)
    except (TypeError, ValueError):
        return jsonify(error="Amount must be a valid number."), 400

    if amount <= 0:
        return jsonify(error="Amount must be greater than zero."), 400

    # Validate title & category length
    if not title:
        return jsonify(error="Title is required."), 400
    if len(title) > 100:
        return jsonify(error="Title cannot exceed 100 characters."), 400

    if not category:
        return jsonify(error="Category is required."), 400
    if len(category) > 50:
        return jsonify(error="Category cannot exceed 50 characters."), 400

    # Validate date format (YYYY-MM-DD)
    if not spent_on:
        return jsonify(error="Date is required."), 400
    try:
        datetime.strptime(spent_on, "%Y-%m-%d")
    except ValueError:
        return jsonify(error="Date must be in YYYY-MM-DD format."), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO expenses (title, amount, category, spent_on) VALUES (?, ?, ?, ?)",
        (title, amount, category, spent_on),
    )
    db.commit()

    return jsonify(id=cur.lastrowid, message="Expense added successfully."), 201


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    db = get_db()
    cur = db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()

    if cur.rowcount == 0:
        return jsonify(error="Expense not found."), 404

    return "", 204


@app.route("/api/summary", methods=["GET"])
def summary():
    """Compute spending summary grouped by category."""
    rows = get_db().execute(
        "SELECT category, ROUND(SUM(amount), 2) AS total, COUNT(*) as count "
        "FROM expenses "
        "GROUP BY category "
        "ORDER BY total DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200


# Initialize database schema on startup
init_db()

if __name__ == "__main__":
    app.run(debug=True)

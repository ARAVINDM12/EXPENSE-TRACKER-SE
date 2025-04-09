from Imports.imports import *
import os
import sys

def get_db_connection():
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)  # For when running as .exe
    else:
        # Go two levels up from ExpenseApp/database/db.py → to EXPENSE-TRACKER-SE
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    db_path = os.path.join(BASE_DIR, "expenses.db")
    print("✅ Using database at:", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        time TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT,
                        expense_type TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        budget_type TEXT,
                        category TEXT,
                        amount REAL)''')

    conn.commit()
    return conn, cursor

conn, cursor = get_db_connection()

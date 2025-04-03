from Imports.imports import *

# Function to establish and return a single database connection
def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    # Ensure tables exist
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

# Establish connection when module is imported
conn, cursor = get_db_connection()

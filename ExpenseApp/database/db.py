from Imports.imports import *
import os
import sys

def get_db_connection():
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)  # For when running as .exe
    else:
        # Go two levels up from ExpenseApp/database/db.py → to EXPENSE-TRACKER-SE
        BASE_DIR = os.path.dirname(__file__)

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

# Function to fetch total income based on date range
def get_total_income(start_date, end_date):

    query = """
    SELECT SUM(amount) FROM expenses
    WHERE expense_type = 'Income' AND date BETWEEN ? AND ?
    """

    cursor.execute(query, (start_date, end_date))
    income_result = cursor.fetchone()

    return income_result[0] if income_result[0] else 0  # Return 0 if no result is found

# Function to fetch total expense based on date range
def get_total_expense(start_date, end_date):

    query = """
    SELECT SUM(amount) FROM expenses
    WHERE expense_type = 'Expense' AND date BETWEEN ? AND ?
    """

    cursor.execute(query, (start_date, end_date))
    expense_result = cursor.fetchone()

    return expense_result[0] if expense_result[0] else 0  # Return 0 if no result is found

# Function to fetch category-wise expense data between two dates
def get_expense_summary_by_category(start_date, end_date):

    query = """
    SELECT category, SUM(amount)
    FROM expenses
    WHERE date BETWEEN ? AND ?
    GROUP BY category
    ORDER BY category ASC
    """

    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()

    return data

# Function to fetch all expense records between two dates, ordered by latest first
def get_all_expenses_between_dates(start_date, end_date):

    cursor.execute("""
        SELECT date, time, category, amount, description, expense_type
        FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC, time DESC
    """, (start_date, end_date))

    records = cursor.fetchall()

    return records

# Function to fetch all budget records
def get_all_budgets():

    cursor.execute("SELECT id, budget_type, category, amount FROM budgets")
    records = cursor.fetchall()

    return records

def get_all_expenses():

    cursor.execute("""
        SELECT id, date, time, category, amount, description, expense_type
        FROM expenses
        ORDER BY date DESC, time DESC
    """)
    records = cursor.fetchall()

    return records

# Function to get total expense amount
def get_total_expense_amount():

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE expense_type = 'Expense'")
    total_expense = cursor.fetchone()[0] or 0.0

    
    return total_expense

def get_total_income_amount():
    

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE expense_type = 'Income'")
    total_expense = cursor.fetchone()[0] or 0.0

    
    return total_expense
# Function to get a single expense record by ID
def get_expense_by_id(expense_id):
    cursor.execute("SELECT date, time, category, amount, description FROM expenses WHERE id=?", (expense_id,))
    record = cursor.fetchone()

    
    return record

def delete_expense_by_id(expense_id):

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

def get_budget_amount(budget_type, category):

    cursor.execute(
        "SELECT amount FROM budgets WHERE budget_type = ? AND category = ?",
        (budget_type, category)
    )
    result = cursor.fetchone()
    return result[0] if result else 0.0

# Function to update an existing expense entry by ID
def update_expense(expense_id, date, time, category, amount, description):

    cursor.execute("""
        UPDATE expenses
        SET date = ?, time = ?, category = ?, amount = ?, description = ?
        WHERE id = ?
    """, (date, time, category, amount, description, expense_id))

    conn.commit()
    

# Function to insert a new budget entry
def insert_budget(budget_type, category, amount):
    

    cursor.execute(
        "INSERT INTO budgets (budget_type, category, amount) VALUES (?, ?, ?)",
        (budget_type, category, amount)
    )

    conn.commit()
    

def update_expense(date, time, category, amount, description, expense_id):
    
    cursor.execute("""
        UPDATE expenses
        SET date=?, time=?, category=?, amount=?, description=? 
        WHERE id=?
    """, (date, time, category, amount, description, expense_id))
    conn.commit()
    

def insert_expense(date, time, category, amount, description, expense_type):
    cursor.execute("""
        INSERT INTO expenses (date, time, category, amount, description, expense_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, time, category, amount, description, expense_type))
    conn.commit()


def get_total_expense_between_dates(start_date, end_date):
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (str(start_date), str(end_date)))
    conn.commit()
    


def delete_budget_by_id(budget_id):
    cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    conn.commit()
    


    
def get_total_spent(cursor, start_date, end_date, category="All"):
    if category == "All":
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (str(start_date), str(end_date)))
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? AND category = ?", 
                       (str(start_date), str(end_date), category))

    total_spent_result = cursor.fetchone()
    total_spent = total_spent_result[0] if total_spent_result and total_spent_result[0] else 0.0

    return total_spent

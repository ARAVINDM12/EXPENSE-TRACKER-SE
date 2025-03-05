import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Add the expense_type column if it doesn't exist
try:
    cursor.execute("ALTER TABLE expenses ADD COLUMN expense_type TEXT DEFAULT 'Expense'")
    conn.commit()
    print("Column 'expense_type' added successfully!")
except sqlite3.OperationalError:
    print("Column 'expense_type' already exists.")

conn.close()

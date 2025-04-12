import sqlite3

# Connect to the old database (outside the ExpenseApp folder)
old_db_path = 'C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\expenses.db'  # Replace with the correct path
old_conn = sqlite3.connect(old_db_path)
old_cursor = old_conn.cursor()

# Connect to the new database (inside ExpenseApp folder)
new_db_path = 'C:\\ARAVIND\\PROJECT\\SE\\EXPENSE-TRACKER-SE\\ExpenseApp\\database\\expenses.db'  # Replace with the correct path
new_conn = sqlite3.connect(new_db_path)
new_cursor = new_conn.cursor()

# Fetch all data from the old 'expense' table
old_cursor.execute("SELECT * FROM expenses")
rows = old_cursor.fetchall()

# Insert the data into the new 'expense' table
for row in rows:
    new_cursor.execute("INSERT INTO expenses (id, date, time, category, amount, description, expense_type) VALUES (?, ?, ?, ?, ?, ?, ?)", row)

# Fetch all data from the old 'budget' table
old_cursor.execute("SELECT * FROM budgets")
rows = old_cursor.fetchall()

# Insert the data into the new 'budget' table
for row in rows:
    new_cursor.execute("INSERT INTO budgets (id, budget_type, category, amount) VALUES (?, ?, ?, ?)", row)

# Commit the changes to the new database
new_conn.commit()

# Close the connections
old_conn.close()
new_conn.close()

print("Data copied successfully!")

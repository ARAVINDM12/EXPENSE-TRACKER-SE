from Imports.imports import *
from UI.ui_components import *
from database.db import conn, cursor

class ExpenseTracker(BoxLayout):
    def __init__(self, screen_manager, cursor, conn, **kwargs): # Added cursor and conn
        super().__init__(orientation='vertical', padding=50, spacing=20, **kwargs)
        self.background_color = '#262626'
        self.screen_manager = screen_manager
        self.cursor = cursor # Added this line
        self.conn = conn # Added this line

        # Get current date and time
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_day = now.strftime("%d")
        current_month = now.strftime("%m")
        current_year = now.strftime("%Y")
        current_hour = now.strftime("%I")  # 12-hour format
        current_minute = now.strftime("%M")
        current_ampm = now.strftime("%p")

        # Header
        self.add_widget(StylishLabel(text="EXPENSE TRACKER"))

        # Input Layout
        input_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height=350)
        input_style = {'size_hint_y': None, 'height': 50, 'font_size': 18, 'foreground_color': (0.9, 0.9, 0.9, 1),
                       'background_color': (0, 0, 0, 1), 'padding': [15, 15], 'halign': 'center'}

        # Date Selection
        self.day_spinner = ModernSpinner(text=current_day, values=[str(i).zfill(2) for i in range(1, 32)])
        self.month_spinner = ModernSpinner(text=current_month, values=[str(i).zfill(2) for i in range(1, 13)])
        self.year_spinner = ModernSpinner(text=current_year, values=[str(i) for i in range(2000, 2051)])

        date_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=50)
        date_layout.add_widget(self.day_spinner)
        date_layout.add_widget(self.month_spinner)
        date_layout.add_widget(self.year_spinner)

        input_layout.add_widget(CustomLabel(text='Date:'))
        input_layout.add_widget(date_layout)

        # Time Selection
        self.hour_spinner = ModernSpinner(text=current_hour, values=[str(i).zfill(2) for i in range(1, 13)])
        self.minute_spinner = ModernSpinner(text=current_minute, values=[str(i).zfill(2) for i in range(0, 60)])
        self.ampm_spinner = ModernSpinner(text=current_ampm, values=['AM', 'PM'])

        time_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=50)
        time_layout.add_widget(self.hour_spinner)
        time_layout.add_widget(self.minute_spinner)
        time_layout.add_widget(self.ampm_spinner)

        input_layout.add_widget(CustomLabel(text='Time:'))
        input_layout.add_widget(time_layout)

        # Category Dropdown
        self.category_spinner = ModernSpinner(text='Select Category', values=('Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Others'),
                                         size_hint_y=None, height=50)
        input_layout.add_widget(CustomLabel(text='Category:'))
        input_layout.add_widget(self.category_spinner)

        # Amount and Description Fields
        self.amount_input = TextInput(hint_text='Amount',**input_style)
        self.desc_input = TextInput(hint_text='Description', **input_style)
        # Expense Type Dropdown
        self.expense_type_spinner = ModernSpinner(
            text="Expense/Income",
            values=("Expense", "Income"),
        )
        input_layout.add_widget(CustomLabel(text='Amount:'))
        input_layout.add_widget(self.amount_input)
        input_layout.add_widget(CustomLabel(text='Description:'))
        input_layout.add_widget(self.desc_input)
        input_layout.add_widget(CustomLabel(text='Type:'))
        input_layout.add_widget(self.expense_type_spinner)

        self.add_widget(input_layout)

        # Buttons
        button_layout = GridLayout(cols=4, spacing=15, size_hint_y=None, height=60)  # changed to 4 columns.
        self.add_button = Button(text='Add',background_normal='',background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.add_button.bind(on_press=self.add_expense)

        self.update_button = Button(text='Update',background_normal='', background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.update_button.bind(on_press=self.open_history_page)

        self.delete_button = Button(text='Delete',background_normal='', background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.delete_button.bind(on_press=self.open_history_page)  # Change function to open history

        self.history_button = Button(text='View History', background_normal='',background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.history_button.bind(on_press=self.view_history)

        self.budget_button = Button(text='Set Budget',background_normal='',background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.budget_button.bind(on_press=self.open_budget_page)  # new button and binding.

        self.view_budget_button = Button(text='View Budgets',background_normal='', background_color=(0, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.view_budget_button.bind(on_press=self.open_view_budgets_page)  # new button and binding.

        self.reports_button = Button(text='Generate Reports',background_normal='', background_color=(0, 0, 0, 1),font_size=18, bold=True, size_hint_y=None, height=50)
        self.reports_button.bind(on_press=self.open_reports_page)  # Bind to the function

        button_layout.add_widget(self.add_button)
        button_layout.add_widget(self.update_button)
        button_layout.add_widget(self.delete_button)
        button_layout.add_widget(self.history_button)
        button_layout.add_widget(self.budget_button)  # add the budget button.
        button_layout.add_widget(self.view_budget_button)  # add the view budget button.
        button_layout.add_widget(self.reports_button)  # Add button to layout

        self.add_widget(BoxLayout(size_hint_y=0.1))  # Spacer
        self.add_widget(button_layout)
        self.add_widget(BoxLayout(size_hint_y=1))  # Spacer
    
    def check_budget(self, date_obj, category, amount):
        assert isinstance(amount, float), "Amount should be a float in check_budget"
        cursor = self.cursor
        conn = self.conn
        try:
            # Daily Check
            self.check_daily_budgets(cursor, date_obj, category, amount)

            # Weekly Check
            start_week = date_obj - timedelta(days=date_obj.weekday())
            end_week = start_week + timedelta(days=6)
            self.check_weekly_budgets(cursor, start_week, end_week, category, amount)

            # Monthly Check
            start_month = date_obj.replace(day=1)
            end_month = (start_month.replace(month=start_month.month + 1) - timedelta(days=1))
            self.check_monthly_budgets(cursor, start_month, end_month, category, amount)

            # Yearly Check
            start_year = date_obj.replace(month=1, day=1)
            end_year = date_obj.replace(month=12, day=31)
            self.check_yearly_budgets(cursor, start_year, end_year, category, amount)

        except sqlite3.Error as e:
            print(f"Database error during budget check: {e}")
            self.show_popup("Database Error", f"Database error: {e}")
        except Exception as e:
            print(f"Error checking budget: {e}")
            self.show_popup("Error", f"Error checking budget: {e}")

    def check_daily_budgets(self, cursor, date_obj, category, amount):
        self.check_budget_type(cursor, date_obj, date_obj, "Daily", category, amount)
        if category != "All":
            self.check_budget_type(cursor, date_obj, date_obj, "Daily", "All", amount)

    def check_weekly_budgets(self, cursor, start_week, end_week, category, amount):
        self.check_budget_type(cursor, start_week, end_week, "Weekly", category, amount)
        if category != "All":
            self.check_budget_type(cursor, start_week, end_week, "Weekly", "All", amount)

    def check_monthly_budgets(self, cursor, start_month, end_month, category, amount):
        self.check_budget_type(cursor, start_month, end_month, "Monthly", category, amount)
        if category != "All":
            self.check_budget_type(cursor, start_month, end_month, "Monthly", "All", amount)

    def check_yearly_budgets(self, cursor, start_year, end_year, category, amount):
        self.check_budget_type(cursor, start_year, end_year, "Yearly", category, amount)
        if category != "All":
            self.check_budget_type(cursor, start_year, end_year, "Yearly", "All", amount)

    def check_budget_type(self, cursor, start_date, end_date, budget_type, category, amount):
        assert isinstance(amount, float), "Amount should be a float in check_budget_type"

        # Fetch the budget amount for the given category
        cursor.execute("SELECT amount FROM budgets WHERE budget_type = ? AND category = ?", (budget_type, category))
        budget_result = cursor.fetchone()
        
        if budget_result:
            budget_amount = float(budget_result[0])

            # Fetch total spent BEFORE adding the new expense
            if category == "All":
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (str(start_date), str(end_date)))
            else:
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? AND category = ?", (str(start_date), str(end_date), category))

            total_spent_result = cursor.fetchone()
            total_spent = total_spent_result[0] if total_spent_result and total_spent_result[0] else 0.0

            # ✅ Fix: Avoid double counting by checking if the amount is already included
            if total_spent < amount:
                total_spent += amount  

            # Calculate exceeded amount correctly
            if total_spent > budget_amount:
                exceeded_by = total_spent - budget_amount
                self.show_popup("Overspending", 
                    f"You've exceeded your {budget_type} budget for {category} by ₹{exceeded_by:.2f}!\n"
                    f"Total Spent: ₹{total_spent:.2f}\n"
                    f"Budget: ₹{budget_amount:.2f}"
                )



    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(600, 300))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def add_expense(self, instance):
        date = f"{self.year_spinner.text}-{self.month_spinner.text}-{self.day_spinner.text}"
        time = f"{self.hour_spinner.text}:{self.minute_spinner.text} {self.ampm_spinner.text}"
        category = self.category_spinner.text.strip()
        amount = self.amount_input.text.strip()
        description = self.desc_input.text.strip()
        expense_type = self.expense_type_spinner.text.strip()

        if category == "Select Category" or not amount or not description:
            self.show_popup("Input Error", "Some fields are empty!")
            return

        try:
            amount = float(amount)  # Convert amount to float and assign back to amount
        except ValueError:
            self.show_popup("Input Error", "Amount must be a numeric value.")
            return

        try:
            if hasattr(self, "selected_expense_id") and self.selected_expense_id:
                self.cursor.execute("UPDATE expenses SET date=?, time=?, category=?, amount=?, description=? WHERE id=?",
                                    (date, time, category, amount, description, self.selected_expense_id))
                self.conn.commit()
                self.show_popup("Expense Updated", "Expense updated successfully!")
                self.selected_expense_id = None
            else:
                self.cursor.execute("INSERT INTO expenses (date, time, category, amount, description, expense_type) VALUES (?, ?, ?, ?, ?, ?)",
                                    (date, time, category, amount, description, expense_type))
                self.conn.commit()
                self.show_popup(f"{expense_type} Added", f"{expense_type} added successfully!")
            
            self.expense_type_spinner="Expense/Income"
            self.category_spinner.text = "Select Category"
            self.amount_input.text = ""
            self.desc_input.text = ""

            history_screen = self.screen_manager.get_screen("history")
            history_screen.load_history()

            # Check budget after adding/updating expense
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            self.check_budget(date_obj, category, amount)

        except sqlite3.Error as e:
            self.show_popup("Database Error", f"Database error: {e}")
        except Exception as e:
            self.show_popup("Database Error", f"Error: {e}")
    

    def open_view_budgets_page(self, instance):
        budgets_screen = self.screen_manager.get_screen("view_budgets")
        budgets_screen.load_budgets()
        self.screen_manager.current = "view_budgets"
    
    def open_reports_page(self, instance):
        self.screen_manager.current = 'reports'  # Navigate to ReportsScreen


    def open_budget_page(self, instance):
        self.screen_manager.current = "budgets"

    

    





    def open_history_page(self, instance):
        history_screen = self.screen_manager.get_screen("history")
        history_screen.load_history()

        if instance == self.update_button:
            history_screen.delete_button.text = "Update Selected"
            history_screen.delete_button.background_color = self.update_button.background_color
            history_screen.delete_button.unbind(on_press=history_screen.delete_selected_expense)
            # Corrected line: Use lambda to capture expense_id
            history_screen.delete_button.bind(on_press=lambda instance: history_screen.load_expense_for_editing())
        else:
            history_screen.delete_button.text = "Delete Selected"
            history_screen.delete_button.background_color = self.delete_button.background_color
            history_screen.delete_button.unbind(on_press=history_screen.load_expense_for_editing)
            history_screen.delete_button.bind(on_press=history_screen.delete_selected_expense)

        history_screen.delete_button.opacity = 1
        history_screen.delete_button.disabled = False
        self.screen_manager.current = "history"




    def clear_fields(self, *fields):
        for field in fields:
            field.text = ""

    def update_expense(self, instance):
        if not hasattr(self, "selected_expense_id") or not self.selected_expense_id:
            print("No expense selected for update.")
            return

        date = f"{self.year_spinner.text}-{self.month_spinner.text}-{self.day_spinner.text}"
        time = f"{self.hour_spinner.text}:{self.minute_spinner.text} {self.ampm_spinner.text}"
        category = self.category_spinner.text.strip()
        amount = self.amount_input.text.strip()
        description = self.desc_input.text.strip()

        if category == "Select Category" or not amount:
            print("Error: Some fields are empty!")
            return

        try:
            amount = float(amount)  # Convert amount to float

            cursor.execute("""
                UPDATE expenses 
                SET date=?, time=?, category=?, amount=?, description=? 
                WHERE id=?
            """, (date, time, category, amount, description, self.selected_expense_id))
            conn.commit()

            print("Expense updated successfully!")

            self.selected_expense_id = None  # Clear selection
            self.amount_input.text = ""
            self.desc_input.text = ""

            # Refresh history screen
            history_screen = self.screen_manager.get_screen("history")
            history_screen.load_history()

            # Navigate back to history page
            self.screen_manager.current = "history"

        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
        except Exception as e:
            print("Error while updating:", e)



    


    def delete_expense(self, instance):
        if not self.selected_expense_id:
            return
        
        try:
            cursor.execute("DELETE FROM expenses WHERE id=?", (self.selected_expense_id,))
            conn.commit()
            print("Expense deleted successfully!")
            self.selected_expense_id = None
        except Exception as e:
            print("Error:", e)

    def view_history(self, instance):
        history_screen = self.screen_manager.get_screen("history")
        history_screen.load_history()
        history_screen.delete_button.opacity = 0  # Hide delete button
        history_screen.delete_button.disabled = True
        self.screen_manager.current = "history"

    def open_update_page(self, instance):
        self.screen_manager.current = "history"  # Open history screen
        history_screen = self.screen_manager.get_screen("history")
        history_screen.set_update_mode(True)  # Enable update mode

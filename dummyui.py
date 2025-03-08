import sqlite3
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle,Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from kivy.uix.popup import Popup
from collections import defaultdict
import datetime
from datetime import  timedelta
import matplotlib.pyplot as plt
from kivy.utils import get_color_from_hex




# Set window background color
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark theme

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    time TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT,
                    expense_type TEXT)''')
conn.commit()

class StylishLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 45  # Bigger font for better visibility
        self.bold = True
        self.color = (0.9, 0.9, 0.9, 1)  # Soft white text
        self.size_hint_y = None
        self.height = 90

        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)  # Dark gray background
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.font_size = 18
        self.color = (0, 1, 1, 1)  # Bright cyan text
        self.bold = True
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size



class ExpenseTracker(BoxLayout):
    def __init__(self, screen_manager, cursor, conn, **kwargs): # Added cursor and conn
        super().__init__(orientation='vertical', padding=50, spacing=20, **kwargs)
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
        input_style = {'size_hint_y': None, 'height': 50, 'font_size': 18, 'foreground_color': (1, 1, 1, 1),
                       'background_color': (0.4, 0.4, 0.4, 1), 'padding': [15, 15], 'halign': 'center'}

        # Date Selection
        self.day_spinner = Spinner(text=current_day, values=[str(i).zfill(2) for i in range(1, 32)], size_hint_y=None, height=50)
        self.month_spinner = Spinner(text=current_month, values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height=50)
        self.year_spinner = Spinner(text=current_year, values=[str(i) for i in range(2000, 2051)], size_hint_y=None, height=50)

        date_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=50)
        date_layout.add_widget(self.day_spinner)
        date_layout.add_widget(self.month_spinner)
        date_layout.add_widget(self.year_spinner)

        input_layout.add_widget(CustomLabel(text='Date:'))
        input_layout.add_widget(date_layout)

        # Time Selection
        self.hour_spinner = Spinner(text=current_hour, values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height=50)
        self.minute_spinner = Spinner(text=current_minute, values=[str(i).zfill(2) for i in range(0, 60)], size_hint_y=None, height=50)
        self.ampm_spinner = Spinner(text=current_ampm, values=['AM', 'PM'], size_hint_y=None, height=50)

        time_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=50)
        time_layout.add_widget(self.hour_spinner)
        time_layout.add_widget(self.minute_spinner)
        time_layout.add_widget(self.ampm_spinner)

        input_layout.add_widget(CustomLabel(text='Time:'))
        input_layout.add_widget(time_layout)

        # Category Dropdown
        self.category_spinner = Spinner(text='Select Category', values=('Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Others'),
                                         size_hint_y=None, height=50)
        input_layout.add_widget(CustomLabel(text='Category:'))
        input_layout.add_widget(self.category_spinner)

        # Amount and Description Fields
        self.amount_input = TextInput(hint_text='Amount', **input_style)
        self.desc_input = TextInput(hint_text='Description', **input_style)
        # Expense Type Dropdown
        self.expense_type_spinner = Spinner(
            text="Expense",
            values=("Expense", "Income"),
            size_hint_y=None,
            height=50
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
        self.add_button = Button(text='Add', background_color=(0, 0.8, 0.2, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.add_button.bind(on_press=self.add_expense)

        self.update_button = Button(text='Update', background_color=(1, 0.6, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.update_button.bind(on_press=self.open_history_page)

        self.delete_button = Button(text='Delete', background_color=(1, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.delete_button.bind(on_press=self.open_history_page)  # Change function to open history

        self.history_button = Button(text='View History', background_color=(0.2, 0.4, 0.8, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.history_button.bind(on_press=self.view_history)

        self.budget_button = Button(text='Set Budget', background_color=(0.8, 0.4, 0.2, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.budget_button.bind(on_press=self.open_budget_page)  # new button and binding.

        self.view_budget_button = Button(text='View Budgets', background_color=(0.4, 0.6, 0.8, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.view_budget_button.bind(on_press=self.open_view_budgets_page)  # new button and binding.

        self.reports_button = Button(text='Generate Reports', background_color=(0, 1, 0, 1),font_size=18, bold=True, size_hint_y=None, height=50)
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

        cursor.execute("SELECT amount FROM budgets WHERE budget_type = ? AND (category = ? OR category = 'All')", (budget_type, category))
        budget_result = cursor.fetchone()

        if budget_result:
            budget_amount = float(budget_result[0])

            if category == "All":
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (str(start_date), str(end_date)))
            else:
                cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ? AND category = ?", (str(start_date), str(end_date), category))

            total_spent_result = cursor.fetchone()
            total_spent = total_spent_result[0] if total_spent_result and total_spent_result[0] else 0.0

            if total_spent + amount > budget_amount:
                exceeded_by = (total_spent + amount) - budget_amount
                self.show_popup("Overspending", f"You've exceeded your {budget_type} budget for {category} by {exceeded_by:.2f}!")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(600, 300))
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    

    def open_view_budgets_page(self, instance):
        budgets_screen = self.screen_manager.get_screen("view_budgets")
        budgets_screen.load_budgets()
        self.screen_manager.current = "view_budgets"
    
    def open_reports_page(self, instance):
        self.screen_manager.current = 'reports'  # Navigate to ReportsScreen


    def open_budget_page(self, instance):
        self.screen_manager.current = "budgets"

    

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
class ViewBudgetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))

        layout.add_widget(StylishLabel(text="Budget List"))

        scroll_view = ScrollView(size_hint_y=1, pos_hint={'top': 1})
        self.budgets_list = GridLayout(cols=4, spacing=10, size_hint_y=None) #increased cols to 4
        self.budgets_list.bind(minimum_height=self.budgets_list.setter('height'))
        scroll_view.add_widget(self.budgets_list)

        layout.add_widget(scroll_view)

        back_button = Button(text="Back", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def load_budgets(self):
        try:
            self.budgets_list.clear_widgets()
            self.budgets_list.cols = 4 #Increased to 4

            headers = ["Budget Type", "Category", "Amount", "Action"] # Added "Action" header
            for header in headers:
                label = Label(text=header, bold=True, size_hint_y=None, height=30, color=(0, 1, 1, 1))
                self.budgets_list.add_widget(label)

            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, budget_type, category, amount FROM budgets") #added id to select
            records = cursor.fetchall()

            for row in records:
                budget_id, budget_type, category, amount = row #added budget_id
                labels = [budget_type, category, f"₹{amount}"]

                for text in labels:
                    label = Label(text=text, size_hint_y=None, height=30, color=(0.5, 0.5, 0.5, 1), font_size = 14)
                    self.budgets_list.add_widget(label)

                delete_button = Button(text="X", size_hint_y=None, height=30, background_color=(1, 0, 0, 1))
                delete_button.bind(on_press=lambda instance, budget_id=budget_id: self.delete_budget(budget_id)) #lambda function to pass budget id
                self.budgets_list.add_widget(delete_button)

            self.budgets_list.height = self.budgets_list.minimum_height
            self.budgets_list.parent.scroll_y = 1

        except Exception as e:
            print(f"Error loading budgets: {e}")

    def delete_budget(self, budget_id):
        try:
            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
            conn.commit()
            self.load_budgets() #reload budgets after deletion
        except Exception as e:
            print(f"Error deleting budget: {e}")

    def go_back(self, instance):
        self.manager.current = "main"
        
class BudgetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))

        layout.add_widget(StylishLabel(text="Set Budgets"))

        input_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height=200)

        self.budget_type_spinner = Spinner(text="Daily", values=("Daily", "Weekly", "Monthly", "Yearly"), size_hint_y=None, height=50)
        self.budget_category_spinner = Spinner(text="All", values=("All", "Food", "Transport", "Shopping", "Entertainment", "Bills", "Others"), size_hint_y=None, height=50)
        self.budget_amount_input = TextInput(hint_text="Budget Amount", size_hint_y=None, height=50)

        input_layout.add_widget(CustomLabel(text="Budget Type:"))
        input_layout.add_widget(self.budget_type_spinner)
        input_layout.add_widget(CustomLabel(text="Category:"))
        input_layout.add_widget(self.budget_category_spinner)
        input_layout.add_widget(CustomLabel(text="Amount:"))
        input_layout.add_widget(self.budget_amount_input)

        layout.add_widget(input_layout)

        set_budget_button = Button(text="Set Budget", size_hint_y=None, height=50, background_color=(0.8, 0.4, 0.2, 1))
        set_budget_button.bind(on_press=self.set_budget)
        layout.add_widget(set_budget_button)

        back_button = Button(text="Back", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        layout.add_widget(BoxLayout(size_hint_y=1)) # Spacer to push content to top.

        self.add_widget(layout)

    def set_budget(self, instance):
        # Add your budget setting logic here (database insertion, etc.)
        budget_type = self.budget_type_spinner.text
        category = self.budget_category_spinner.text
        amount = self.budget_amount_input.text
        try:
            amount = float(amount)
            cursor.execute("INSERT INTO budgets (budget_type, category, amount) VALUES (?, ?, ?)", (budget_type, category, amount))
            conn.commit()
            self.show_popup("budget added","budget added successfully")
        except:
            self.show_popup("error", "invalid amount")

    def go_back(self, instance):
        self.manager.current = "main"
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        close_button.bind(on_press=popup.dismiss) # Bind close button to dismiss popup
        popup.open()

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main Vertical Layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title Label (Always on top)
        main_layout.add_widget(Label(text="EXPENSE REPORTS", font_size=24, bold=True, size_hint_y=None, height=75))

        # Charts Box (STRICTLY HALF THE SCREEN)
        self.chart_container = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=10)
        main_layout.add_widget(self.chart_container)

        # Summary Layout (Centered, fills remaining space)
        self.summary_layout = BoxLayout(orientation='vertical', spacing=5, padding=10, size_hint_y=0.2)
        main_layout.add_widget(self.summary_layout)

        # Lower Section (Filters + Buttons)
        lower_section = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=10)
        

        # Filters Layout (Period Selection & Date Inputs)
        filter_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

        # Report Type Dropdown (Half Width)
        self.report_type = Spinner(
            text="Daily",
            values=("Daily", "Weekly", "Monthly", "Yearly", "Custom"),
            size_hint=(0.5, None),
            size=(120, 50)
        )
        filter_layout.add_widget(self.report_type)
        self.report_type.bind(text=self.on_report_type_change)

        # Custom Date Inputs (Evenly Split Other Half)
        date_inputs_layout = BoxLayout(size_hint=(0.5, None), height=40, spacing=10)
        self.start_date_input = TextInput(hint_text="Start Date (YYYY-MM-DD)", size_hint=(0.5, None), size=(140, 50))
        self.end_date_input = TextInput(hint_text="End Date (YYYY-MM-DD)", size_hint=(0.5, None), size=(140, 50))
        self.start_date_input.disabled = True
        self.end_date_input.disabled = True
        date_inputs_layout.add_widget(self.start_date_input)
        date_inputs_layout.add_widget(self.end_date_input)
        filter_layout.add_widget(date_inputs_layout)

        lower_section.add_widget(filter_layout)

        # Button Layout (More Evenly Spaced)
        button_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)

        # Generate Reports Button
        self.generate_button = Button(text="Generate Report", background_color=(0, 1, 0, 1))
        self.generate_button.bind(on_press=self.generate_reports)
        button_layout.add_widget(self.generate_button)

        # Export CSV Button
        csv_button = Button(text="Export CSV", background_color=(0.8, 0.5, 0, 1))
        csv_button.bind(on_press=self.export_csv)
        button_layout.add_widget(csv_button)

        # Export PDF Button
        pdf_button = Button(text="Export PDF", background_color=(0.5, 0.2, 0.8, 1))
        pdf_button.bind(on_press=self.export_pdf)
        button_layout.add_widget(pdf_button)

        lower_section.add_widget(button_layout)

        # Back Button (Smaller Height)
        back_button = Button(text="Back", size_hint_x=1, size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        back_button.bind(on_press=self.go_back)
        lower_section.add_widget(back_button)

        main_layout.add_widget(lower_section)
        self.add_widget(main_layout)

        # Generate default daily report
        self.generate_reports(None)

    def on_report_type_change(self, spinner, text):
        if text == "Custom":
            self.start_date_input.disabled = False
            self.end_date_input.disabled = False
        else:
            self.start_date_input.disabled = True
            self.end_date_input.disabled = True

    def generate_reports(self, instance):
        self.chart_container.clear_widgets()
        self.summary_layout.clear_widgets()

        report_type = self.report_type.text
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        data = self.fetch_expense_data(report_type, start_date, end_date)

        if data:
            pie_chart, bar_chart = self.create_charts(data)
            self.chart_container.add_widget(FigureCanvasKivyAgg(pie_chart))
            self.chart_container.add_widget(FigureCanvasKivyAgg(bar_chart))

            pie_summary = self.generate_pie_summary(data)
            bar_summary = self.generate_bar_summary(data)

            # Layout for Summary Boxes
            summaries_box = BoxLayout(orientation='horizontal', spacing=00, padding=(10, 00, 10, 0))

            # Pie Chart Summary Grid
            pie_grid = GridLayout(cols=1, spacing=0, size_hint_x=0.5, padding=(10, 0))

            # Bar Chart Summary Grid
            bar_grid = GridLayout(cols=1, spacing=0, size_hint_x=0.5, padding=(10, 0))

            # Pie Chart Summary Title
            pie_label = Label(text="[b][size=20]Pie Chart Summary[/size][/b]", markup=True, halign='center', size_hint_y=None, height=40)
            pie_grid.add_widget(pie_label)

            # Horizontal Divider
            pie_grid.add_widget(Label(text="--------------------------------------", bold=True, size_hint_y=None, height=20))

            for line in pie_summary.split('\n'):
                if line:
                    category, value_percentage = line.split(': ', 1) if ': ' in line else ("", line)
                    label = Label(text=f"[b]{category}:[/b] {value_percentage}", markup=True, halign='left', valign='middle', size_hint_y=None, height=30)
                    pie_grid.add_widget(label)

            # Bar Chart Summary Title
            bar_label = Label(text="[b][size=20]Bar Chart Summary[/size][/b]", markup=True, halign='center', size_hint_y=None, height=40)
            bar_grid.add_widget(bar_label)

            # Horizontal Divider
            bar_grid.add_widget(Label(text="--------------------------------------", bold=True, size_hint_y=None, height=20))

            for line in bar_summary.split('\n'):
                if line.strip():  # Ensure line is not empty
                    if ': ' in line:
                        category, value_percentage = line.split(': ', 1)
                        label_text = f"[b]{category}:[/b] {value_percentage}"
                    else:
                        label_text = f"[b]{line}[/b]"  # Display without extra colon
                    
                    label = Label(text=label_text, markup=True, halign='left', valign='middle', size_hint_y=None, height=30)
                    bar_grid.add_widget(label)


            # Add Grids to the Summary Box
            summaries_box.add_widget(pie_grid)
            summaries_box.add_widget(bar_grid)

            # Add Spacing & Summaries to Layout
            spacer = Label(size_hint_y=None, height=40)
            self.summary_layout.add_widget(spacer)
            self.summary_layout.add_widget(summaries_box)

            # Adjust height based on content
            self.summary_layout.height = self.summary_layout.minimum_height

        else:
            popup = Popup(title="No Data", content=Label(text="No expenses found for the selected period."), size_hint=(0.6, 0.3))
            popup.open()

    def generate_pie_summary(self, data):
        if not data:
            return "No pie chart data available."

        total_expenses = sum(amount for _, amount in data)
        category_summaries = ""

        for category, amount in data:
            percentage = (amount / total_expenses) * 100
            category_summaries += f"{category}: [b]{amount:.2f} ({percentage:.2f}%)[/b]\n"

        return f"{category_summaries}"

    def generate_bar_summary(self, data):
        if not data:
            return "No bar chart data available."

        total_expenses = sum(amount for _, amount in data)
        income = total_expenses * 1.2
        expense = total_expenses

        income_percentage = (income / (income + expense)) * 100
        expense_percentage = (expense / (income + expense)) * 100

        return f"[b]Total Income:[/b] {income:.2f} ({income_percentage:.2f}%)\n[b]Total Expense:[/b] {expense:.2f} ({expense_percentage:.2f}%)"
    
    def fetch_expense_data(self, report_type, start_date, end_date):
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        query = """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY category ASC
        """
        if report_type == "Daily":
            start_date = end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Weekly":
            start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Monthly":
            start_date = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Yearly":
            start_date = (datetime.date.today().replace(month=1, day=1)).strftime("%Y-%m-%d")
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        elif report_type == "Custom":
            if not start_date or not end_date:
                return None

        cursor.execute(query, (start_date, end_date))
        data = cursor.fetchall()
        conn.close()
        return data

    def create_charts(self, data):
        categories, values = zip(*data) if data else ([], [])
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
        ax1.set_title("Category-wise Expense Breakdown")
        fig2, ax2 = plt.subplots()
        ax2.bar(["Total Income", "Total Expense"], [sum(values), sum(values) * 1.2], color=["green", "red"])
        ax2.set_title("Total Income vs Expense")
        return fig1, fig2

    def export_csv(self, instance):
        pass

    def export_pdf(self, instance):
        pass

    def go_back(self, instance):
        self.manager.current = 'main'


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1)) # Add size_hint

        # Header
        layout.add_widget(StylishLabel(text="Expense History"))
        # Total Expense, Income, Net Labels in a Horizontal BoxLayout
        totals_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50) #Horizontal boxlayout for totals.
        # Total Expense Label
        self.total_expense_label = Label(text="Total Expense: ₹0.00", font_size=20, bold=True, color=(1, 1, 0, 1),
                                         size_hint_y=None, height=50)
        totals_layout.add_widget(self.total_expense_label)

        #Total Income Label
        self.total_income_label = Label(text="Total Income: ₹0.00", font_size=20, bold=True, color=(1, 1, 0, 1),
                                         size_hint_y=None, height=50)
        totals_layout.add_widget(self.total_income_label)

        #Net Label
        self.net_label = Label(text="Net: ₹0.00", font_size=20, bold=True, color=(1, 1, 0, 1),
                                         size_hint_y=None, height=50)
        totals_layout.add_widget(self.net_label)

        layout.add_widget(totals_layout) #Add the horizontal layout containing totals.
        # Scrollable List
        scroll_view = ScrollView(size_hint_y=1, pos_hint={'top': 1}) # Add pos_hint to align top
        self.history_list = GridLayout(cols=7, spacing=10, size_hint_y=None)  # Create GridLayout
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        scroll_view.add_widget(self.history_list)
        
        layout.add_widget(scroll_view)

        # Delete Button
        self.delete_button = Button(text="Delete Selected", size_hint_y=None, height=50, background_color=(1, 0, 0, 1))
        self.delete_button.bind(on_press=self.delete_selected_expense)
        layout.add_widget(self.delete_button)

        # Back Button
        back_button = Button(text="Back", size_hint_y=None, height=50, background_color=(0.2, 0.6, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
        self.selected_expense_id = None  # Store selected expense ID
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint_y=None, height=40)
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        close_button.bind(on_press=popup.dismiss) # Bind close button to dismiss popup
        popup.open()
    
    def load_history(self):
        try:
            self.history_list.clear_widgets()
            self.history_list.cols = 7

            headers = ["Date", "Time", "Category", "Amount", "Description", "Expense Type", "Select"]
            for header in headers:
                label = Label(text=header, bold=True, size_hint_y=None, height=30, color=(0, 1, 1, 1))
                self.history_list.add_widget(label)

            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, time, category, amount, description, expense_type FROM expenses ORDER BY date DESC, time DESC")
            records = cursor.fetchall()

            records_by_date = defaultdict(list)
            for row in records:
                date_obj = datetime.datetime.strptime(row[1], "%Y-%m-%d").date()
                records_by_date[date_obj].append(row)

            for date_obj, daily_records in records_by_date.items():
                date_str = date_obj.strftime("%Y-%m-%d")

                # Calculate empty label count for each side.
                empty_count = (self.history_list.cols - 1) // 2

                # Add empty labels for the left side
                for _ in range(empty_count):
                    self.history_list.add_widget(Label(text="", size_hint_y=None, height=30))

                # Add separator label
                separator_label = Label(
                    text=f" ────────────────── {date_str} ────────────────── ",
                    bold=True,
                    size_hint_y=None,
                    height=30,
                    color=(0.5, 0.5, 0.5, 1),
                    font_size=22,
                )
                self.history_list.add_widget(separator_label)

                # Add empty labels for the right side
                for _ in range(self.history_list.cols - 1 - empty_count):
                    self.history_list.add_widget(Label(text="", size_hint_y=None, height=30))

                for row in daily_records:
                    expense_id, date, time, category, amount, description, expense_type = row
                    color = (1, 0, 0, 1) if expense_type == "Expense" else (0, 1, 0, 1)
                    labels = [date, time, category, f"₹{amount}", description, expense_type]

                    for text in labels:
                        label = Label(text=text, size_hint_y=None, height=30, color=color)
                        self.history_list.add_widget(label)

                    select_button = Button(text="Select", size_hint_y=None, height=30, background_color=(0.3, 0.3, 0.3, 1))
                    select_button.bind(on_press=lambda instance, eid=expense_id: self.select_expense_for_delete(eid, instance))
                    self.history_list.add_widget(select_button)

            # Calculate total expense, total income, and net
            cursor.execute("SELECT SUM(amount) FROM expenses WHERE expense_type = 'Expense'")
            total_expense = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT SUM(amount) FROM expenses WHERE expense_type = 'Income'")
            total_income = cursor.fetchone()[0] or 0.0

            net = total_income - total_expense

            # Update labels
            self.total_expense_label.text = f"Total Expense: ₹{total_expense:.2f}"
            self.total_income_label.text = f"Total Income: ₹{total_income:.2f}"
            self.net_label.text = f"Net: ₹{net:.2f}"

            conn.close()

            if not records:
                no_data_label = Label(text="No history found.", font_size=18, color=(1, 1, 1, 1), size_hint_y=None, height=30)
                self.history_list.add_widget(no_data_label)
                for _ in range(6):
                    self.history_list.add_widget(Label(text=""))

            self.history_list.height = self.history_list.minimum_height
            self.history_list.parent.scroll_y = 1

        except Exception as e:
            print(f"Error loading history: {e}")



    def select_expense(self, expense_id, instance, update_mode=False):
        if hasattr(self, 'selected_button') and self.selected_button:
            self.selected_button.background_color = (0.3, 0.3, 0.3, 1)  # Reset previous selection

        self.selected_expense_id = expense_id
        self.selected_button = instance
        self.selected_button.background_color = (1, 0, 0, 1)  # Highlight selected

        if update_mode:
            # Retrieve expense details and populate main screen
            cursor.execute("SELECT date, time, category, amount, description FROM expenses WHERE id=?", (expense_id,))
            record = cursor.fetchone()

            if record:
                date, time, category, amount, description = record
                expense_tracker = self.manager.get_screen("main").children[0]  # Get main screen's ExpenseTracker instance

                # Split date and time for spinners
                year, month, day = date.split("-")
                hour_minute, am_pm = time.split()
                hour, minute = hour_minute.split(":")

                # Populate fields in main screen
                expense_tracker.year_spinner.text = year
                expense_tracker.month_spinner.text = month
                expense_tracker.day_spinner.text = day
                expense_tracker.hour_spinner.text = hour
                expense_tracker.minute_spinner.text = minute
                expense_tracker.ampm_spinner.text = am_pm
                expense_tracker.category_spinner.text = category
                expense_tracker.amount_input.text = str(amount)
                expense_tracker.desc_input.text = description

                # Store expense ID for update
                expense_tracker.selected_expense_id = expense_id

                # Switch to main screen
                self.manager.current = "main"

        # If update_mode is False (delete or view), nothing happens after highlighting




    def delete_selected_expense(self, instance):
        if not self.selected_expense_id:
            print("No expense selected!")
            return

        try:
            cursor.execute("DELETE FROM expenses WHERE id=?", (self.selected_expense_id,))
            conn.commit()
            print("Expense deleted successfully!")
            self.show_popup("Expense Deleted", "Expense deleted successfully!")

            self.selected_expense_id = None  # Reset selection
            self.load_history()  # Refresh history after deletion

        except Exception as e:
            print("Error:", e)
    
    def set_update_mode(self, update_mode):
        self.update_mode = update_mode


    def go_back(self, instance):
        self.manager.current = "main"

    def load_expense_for_editing(self):
        if not self.selected_expense_id:
            print("No expense selected!")
            return

        cursor.execute("SELECT date, time, category, amount, description FROM expenses WHERE id=?", (self.selected_expense_id,))
        record = cursor.fetchone()
        if record:
            date, time, category, amount, description = record
            main_screen = self.manager.get_screen("main").children[0]  # Get the ExpenseTracker instance

            # Fill the input fields
            main_screen.year_spinner.text, main_screen.month_spinner.text, main_screen.day_spinner.text = date.split("-")

            time_parts = time.split(" ")
            if len(time_parts) == 2:
                hour_minute = time_parts[0].split(":")
                if len(hour_minute) == 2:
                    main_screen.hour_spinner.text = hour_minute[0]
                    main_screen.minute_spinner.text = hour_minute[1]
                    main_screen.ampm_spinner.text = time_parts[1] # AM/PM
                else:
                    print(f"Invalid time format: {time}")
                    return
            elif len(time_parts) == 1: #case where there is no AM/PM
                hour_minute = time_parts[0].split(":")
                if len(hour_minute) == 2:
                    main_screen.hour_spinner.text = hour_minute[0]
                    main_screen.minute_spinner.text = hour_minute[1]
                    main_screen.ampm_spinner.text = "AM" #Default to AM if none is given.
                else:
                    print(f"Invalid time format: {time}")
                    return
            else:
                print(f"Invalid time format: {time}")
                return

            main_screen.category_spinner.text = category
            main_screen.amount_input.text = str(amount)
            main_screen.desc_input.text = description

            main_screen.selected_expense_id = self.selected_expense_id  # Store selected ID

            # Go back to main screen for editing
            self.manager.current = "main"

    def select_expense_for_update(self, expense_id, instance):
        self.select_expense(expense_id, instance, update_mode=True) #called when update button is pressed

    def select_expense_for_delete(self, expense_id, instance):
        self.select_expense(expense_id, instance) #called when history item is pressed for deletion

    def select_expense_for_view(self, expense_id, instance):
        self.select_expense(expense_id, instance) #called when history item is pressed for view

class ExpenseApp(App):
    def build(self):
        try:
            conn = sqlite3.connect("expenses.db")
            cursor = conn.cursor()

            # Create the expenses table (if it doesn't exist)
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                time TEXT,
                                category TEXT,
                                amount REAL,
                                description TEXT,
                                expense_type TEXT)''')

            # Create the budgets table (if it doesn't exist)
            cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                budget_type TEXT,
                                category TEXT,
                                amount REAL)''')

            conn.commit()

            sm = ScreenManager()
            sm.add_widget(Screen(name="main"))
            sm.add_widget(HistoryScreen(name="history"))
            sm.add_widget(BudgetsScreen(name="budgets"))
            sm.add_widget(ViewBudgetsScreen(name="view_budgets"))
            sm.add_widget(ReportsScreen(name='reports'))
            sm.get_screen("main").add_widget(ExpenseTracker(screen_manager=sm, cursor=cursor, conn=conn)) #added cursor and conn

            self.conn = conn  # Store the connection for later use
            return sm

        except sqlite3.Error as e:
            print(f"Database error during initialization: {e}")
            # Consider showing a popup or exiting the app if database setup fails
            return None  # Return None to prevent app from running without database

    def on_stop(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == '__main__':
    ExpenseApp().run()
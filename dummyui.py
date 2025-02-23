import sqlite3
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
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen

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
                    description TEXT)''')
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
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation='vertical', padding=50, spacing=20, **kwargs)
        self.screen_manager = screen_manager

        # Header
        self.add_widget(StylishLabel(text="EXPENSE TRACKER"))

        # Input Layout
        input_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height=350)
        input_style = {'size_hint_y': None, 'height': 50, 'font_size': 18, 'foreground_color': (1, 1, 1, 1),
                       'background_color': (0.4, 0.4, 0.4, 1), 'padding': [15, 15], 'halign': 'center'}

        # Date Input
        self.date_input = TextInput(hint_text="YYYY-MM-DD", **input_style)
        
        # Day, Month, Year Selection
        self.day_spinner = Spinner(text='DD', values=[str(i).zfill(2) for i in range(1, 32)], size_hint_y=None, height=50)
        self.month_spinner = Spinner(text='MM', values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height=50)
        self.year_spinner = Spinner(text='YYYY', values=[str(i) for i in range(2000, 2051)], size_hint_y=None, height=50)

        date_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=50)
        date_layout.add_widget(self.day_spinner)
        date_layout.add_widget(self.month_spinner)
        date_layout.add_widget(self.year_spinner)

        input_layout.add_widget(CustomLabel(text='Date:'))
        input_layout.add_widget(date_layout)

        # Time Input
        self.time_input = TextInput(hint_text="HH:MM AM/PM", **input_style)
        self.hour_spinner = Spinner(text='HH', values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height=50)
        self.minute_spinner = Spinner(text='MM', values=[str(i).zfill(2) for i in range(0, 60)], size_hint_y=None, height=50)
        self.ampm_spinner = Spinner(text='AM/PM', values=['AM', 'PM'], size_hint_y=None, height=50)
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

        input_layout.add_widget(CustomLabel(text='Amount:'))
        input_layout.add_widget(self.amount_input)
        input_layout.add_widget(CustomLabel(text='Description:'))
        input_layout.add_widget(self.desc_input)

        self.add_widget(input_layout)

        # Buttons
        button_layout = GridLayout(cols=3, spacing=15, size_hint_y=None, height=60)
        self.add_button = Button(text='Add', background_color=(0, 0.8, 0.2, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.add_button.bind(on_press=self.add_expense)
        
        self.update_button = Button(text='Update', background_color=(1, 0.6, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.update_button.bind(on_press=self.open_history_page)


        self.delete_button = Button(text='Delete', background_color=(1, 0, 0, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.delete_button.bind(on_press=self.open_history_page)  # Change function to open history

        self.history_button = Button(text='View History', background_color=(0.2, 0.4, 0.8, 1), font_size=18, bold=True, size_hint_y=None, height=50)
        self.history_button.bind(on_press=self.view_history)

        button_layout.add_widget(self.add_button)
        button_layout.add_widget(self.update_button)
        button_layout.add_widget(self.delete_button)
        button_layout.add_widget(self.history_button)
        
        self.add_widget(button_layout)
        self.add_widget(BoxLayout(size_hint_y=1))

    def add_expense(self, instance):
        date = f"{self.year_spinner.text}-{self.month_spinner.text}-{self.day_spinner.text}"
        time = f"{self.hour_spinner.text}:{self.minute_spinner.text} {self.ampm_spinner.text}"
        category = self.category_spinner.text.strip()
        amount = self.amount_input.text.strip()
        description = self.desc_input.text.strip()

        if category == "Select Category" or not amount:
            print("Error: Some fields are empty!")  
            return  

        try:
            if hasattr(self, "selected_expense_id") and self.selected_expense_id:
                cursor.execute("UPDATE expenses SET date=?, time=?, category=?, amount=?, description=? WHERE id=?",
                            (date, time, category, float(amount), description, self.selected_expense_id))
                conn.commit()
                
                print("Expense updated successfully!")

                self.selected_expense_id = None  # Clear selection

            else:
                cursor.execute("INSERT INTO expenses (date, time, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                            (date, time, category, float(amount), description))
                conn.commit()
                print("Expense added successfully!")

            self.amount_input.text = ""
            self.desc_input.text = ""

            # Refresh history page
            history_screen = self.screen_manager.get_screen("history")
            history_screen.load_history()  # <--- Refresh history UI

        except Exception as e:
            print("Error while adding/updating:", e)





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


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Header
        layout.add_widget(StylishLabel(text="Expense History"))

        # Scrollable List
        scroll_view = ScrollView()
        self.history_list = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
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

    def load_history(self):
        self.history_list.clear_widgets()  # Clear previous entries

        cursor.execute("SELECT id, date, time, category, amount, description FROM expenses ORDER BY date DESC")
        records = cursor.fetchall()

        if not records:
            self.history_list.add_widget(Label(text="No history found.", font_size=18, color=(1, 1, 1, 1)))
        else:
            for row in records:
                expense_id, date, time, category, amount, description = row
                expense_text = f"{date} {time} - {category}: ₹{amount} ({description})"

                entry = Button(text=expense_text, size_hint_y=None, height=50, background_color=(0.3, 0.3, 0.3, 1))
                entry.bind(on_press=lambda instance, eid=expense_id: self.select_expense_for_delete(eid, instance)) #changed to the delete call
                self.history_list.add_widget(entry)

        self.history_list.parent.scroll_y = 1  # Scroll to top to show latest


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
        sm = ScreenManager()
        sm.add_widget(Screen(name="main"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.get_screen("main").add_widget(ExpenseTracker(screen_manager=sm))
        return sm

if __name__ == '__main__':
    ExpenseApp().run()
    conn.close()

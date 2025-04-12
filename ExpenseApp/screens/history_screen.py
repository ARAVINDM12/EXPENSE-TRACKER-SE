from Imports.imports import *
from UI.ui_components import *
from database.db import conn, cursor
from database.db import *

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1)) # Add size_hint

        # Header
        layout.add_widget(StylishLabel(text="EXPENSE HISTORY"))
        # Total Expense, Income, Net Labels in a Horizontal BoxLayout
        totals_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50) #Horizontal boxlayout for totals.
        # Total Expense Label
        self.total_expense_label = Label(text="TOTAL EXPENSE: ₹0.00", font_size=20, bold=True, color=(1, 0, 0, 1),
                                         size_hint_y=None, height=50)
        totals_layout.add_widget(self.total_expense_label)

        #Total Income Label
        self.total_income_label = Label(text="TOTAL INCOME: ₹0.00", font_size=20, bold=True, color=(0, 1, 0, 1),
                                         size_hint_y=None, height=50)
        totals_layout.add_widget(self.total_income_label)

        #Net Label
        self.net_label = Label(text="NET: ₹0.00", font_size=20, bold=True, color=(0, 0, 1, 1),
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

            headers = ["DATE", "TIME", "CATEGORY", "AMOUNT", "DESCRIPTION", "EXPENSE TYPE", "SELECT"]
            for header in headers:
                label = Label(text=header, bold=True, size_hint_y=None, height=30, color=(1, 1, 1, 1),halign="left",valign="middle")
                self.history_list.add_widget(label)

            
            
            records = get_all_expenses()

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
                    text=f"────────────────────────────────────────────────────────────────────────────────────────────────────── {date_str} ──────────────────────────────────────────────────────────────────────────────────────────────────────",
                    bold=True,
                    size_hint=(1, None),  # Makes it full width
                    height=30,
                    color=(0.5, 0.5, 0.5, 1),
                    font_size=22,
                    halign='center',
                    valign='middle',
                    text_size=(None, None)  # Ensures proper alignment
                )
                self.history_list.add_widget(separator_label)

                # Add empty labels for the right side
                for _ in range(self.history_list.cols - 1 - empty_count):
                    self.history_list.add_widget(Label(text="", size_hint_y=None, height=30))

                for row in daily_records:
                    expense_id, date, time, category, amount, description, expense_type = row
                    color = (0.5, 0.5, 0.5, 1) if expense_type == "Expense" else (0.5,0.5, 0.5, 1)
                    labels = [date, time, category, f"₹{amount}", description, expense_type]

                    for text in labels:
                        label = Label(text=text, size_hint_y=None, height=30, color=color,halign="left")
                        self.history_list.add_widget(label)

                    select_button = Button(text="Select", size_hint_y=None, height=30, background_color=(0.3, 0.3, 0.3, 1))
                    select_button.bind(on_press=lambda instance, eid=expense_id: self.select_expense_for_delete(eid, instance))
                    self.history_list.add_widget(select_button)


            # Calculate total expense, total income, and net
          
            total_expense = get_total_expense_amount()
            total_income = get_total_income_amount()

            net = total_income - total_expense

            # Update labels
            self.total_expense_label.text = f"TOTAL EXPENSE: ₹{total_expense:.2f}"
            self.total_income_label.text = f"TOTAL INCOME: ₹{total_income:.2f}"
            self.net_label.text = f"NET: ₹{net:.2f}"

            #conn.close()

            if not records:
                no_data_label = Label(text="No history found.", font_size=18, color=(1, 1, 1, 1), size_hint_y=None, height=30)
                self.history_list.add_widget(no_data_label)
                for _ in range(6):
                    self.history_list.add_widget(Label(text=""))

            self.history_list.height = self.history_list.minimum_height
            if self.history_list.parent:
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
            record = get_expense_by_id(expense_id)

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
            delete_expense_by_id(self.selected_expense_id)
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

        record = get_expense_by_id(self.selected_expense_id)
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

from Imports.imports import *
from UI.ui_components import *
from database.db import conn,cursor

class BudgetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))
        self.background_color = '#262626'
        layout.add_widget(StylishLabel(text="Set Budgets"))

        input_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height=200)
        input_style = {'size_hint_y': None, 'height': 50, 'font_size': 18, 'foreground_color': (0.9, 0.9, 0.9, 1),
                       'background_color': (0, 0, 0, 1), 'padding': [15, 15], 'halign': 'center'}
        self.budget_type_spinner = ModernSpinner(text="Select Range", values=("Daily", "Weekly", "Monthly", "Yearly"), size_hint_y=None, height=50)
        self.budget_category_spinner = ModernSpinner(text="Category", values=("All", "Food", "Transport", "Shopping", "Entertainment", "Bills", "Others"), size_hint_y=None, height=50)
        self.budget_amount_input = TextInput(hint_text="Budget Amount",**input_style)

        input_layout.add_widget(CustomLabel(text="Budget Type:"))
        input_layout.add_widget(self.budget_type_spinner)
        input_layout.add_widget(CustomLabel(text="Category:"))
        input_layout.add_widget(self.budget_category_spinner)
        input_layout.add_widget(CustomLabel(text="Amount:"))
        input_layout.add_widget(self.budget_amount_input)

        layout.add_widget(input_layout)

        set_budget_button = Button(text="Set Budget", size_hint_y=None, height=50, background_color=(0, 0, 0, 1))
        set_budget_button.bind(on_press=self.set_budget)
        layout.add_widget(set_budget_button)

        back_button = Button(text="Back", size_hint_y=None, height=50, background_color = (0, 0, 1, 1))
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
        
        self.budget_amount_input.text = ""
        self.budget_type_spinner.text = "Select Range"
        self.budget_category_spinner.text = "Category"


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
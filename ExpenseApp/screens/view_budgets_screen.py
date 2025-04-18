from Imports.imports import *
from UI.ui_components import *
from database.db import conn, cursor
from database.db import *

class ViewBudgetsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(1, 1))

        layout.add_widget(StylishLabel(text="BUDGET LIST"))

        scroll_view = ScrollView(size_hint_y=1, pos_hint={'top': 1})
        self.budgets_list = GridLayout(cols=4, spacing=10, size_hint_y=None) #increased cols to 4
        self.budgets_list.bind(minimum_height=self.budgets_list.setter('height'))
        scroll_view.add_widget(self.budgets_list)

        layout.add_widget(scroll_view)

        back_button = Button(text="Back", size_hint_y=None, height=50, background_color=(0, 0, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def load_budgets(self):
        try:
            self.budgets_list.clear_widgets()
            self.budgets_list.cols = 4 #Increased to 4

            headers = ["BUDGET TYPE", "CATEGORY", "AMOUNT", "ACTION"] # Added "Action" header
            for header in headers:
                label = Label(text=header, bold=True, size_hint_y=None, height=30, color=(1, 1, 1, 1))
                self.budgets_list.add_widget(label)

            #conn = sqlite3.connect("expenses.db")
            #cursor = conn.cursor()
            records = get_all_budgets()

            for row in records:
                budget_id, budget_type, category, amount = row #added budget_id
                labels = [budget_type, category, f"₹{amount}"]

                for text in labels:
                    label = Label(text=text, size_hint_y=None, height=30, color=(0.5, 0.5, 0.5, 1), font_size = 14)
                    self.budgets_list.add_widget(label)

                delete_button = Button(text="X", size_hint_y=None, height=30, background_color=(0, 0, 0, 1))
                delete_button.bind(on_press=lambda instance, budget_id=budget_id: self.confirm_delete(budget_id))
                self.budgets_list.add_widget(delete_button)

            self.budgets_list.height = self.budgets_list.minimum_height
            self.budgets_list.parent.scroll_y = 1

        except Exception as e:
            print(f"Error loading budgets: {e}")

    def delete_budget(self, budget_id):
        try:
        
            delete_budget_by_id(budget_id)
            self.load_budgets() #reload budgets after deletion
        except Exception as e:
            print(f"Error deleting budget: {e}")

    def confirm_delete(self, budget_id):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Are you sure you want to delete this budget?"))
        buttons = BoxLayout(size_hint_y=None, height=40)

        yes_button = Button(text='Yes')
        no_button = Button(text='No')
        buttons.add_widget(yes_button)
        buttons.add_widget(no_button)
        content.add_widget(buttons)

        popup = Popup(title="Confirm Deletion", content=content, size_hint=(None, None), size=(500, 200))
        
        yes_button.bind(on_press=lambda *args: (self.delete_budget(budget_id), popup.dismiss()))
        no_button.bind(on_press=popup.dismiss)
        popup.open()


    def go_back(self, instance):
        self.manager.current = "main"
        
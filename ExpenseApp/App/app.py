from Imports.imports import *
from UI.ui_components import *
from screens.history_screen import *
from screens.reports_screen import *
from screens.view_budgets_screen import *
from screens.expense_tracker import *
from screens.budgets_screen import BudgetsScreen
from database.db import conn, cursor
#from Splashscreen.splash import *

class ExpenseApp(App):
    def build(self):
        try:
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


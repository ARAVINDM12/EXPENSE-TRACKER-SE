from Imports.imports import *
from screens.budgets_screen import BudgetsScreen  # Ensure correct path
from screens.view_budgets_screen import ViewBudgetsScreen
from screens.history_screen import HistoryScreen
from screens.reports_screen import ReportsScreen
from database.db import conn, cursor
from UI.ui_components import *
from screens.expense_tracker import *
from App.app import *  # This might contain your main application logic

if __name__ == '__main__':
    ExpenseApp().run()

    
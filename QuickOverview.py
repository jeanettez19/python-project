import pandas as pd
from datetime import datetime

class QuickOverview:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(file_path, sheet_name=['expense', 'budget'])
        self.expense = self.data['expense']
        self.budget = self.data['budget']

    def get_current_month_overview(self):
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Filter budget data for the current month and year
        self.budget['date'] = pd.to_datetime(self.budget['date'], errors='coerce')
        current_month_budget = self.budget[
            (self.budget['date'].dt.month == current_month) & (self.budget['date'].dt.year == current_year)
        ]
        total_budget = current_month_budget['monthly_budget'].sum()

        # Filter expense data for the current month and year
        self.expense['date'] = pd.to_datetime(self.expense['date'], errors='coerce')
        current_month_expense = self.expense[
            (self.expense['date'].dt.month == current_month) & (self.expense['date'].dt.year == current_year)
        ]
        total_expense = current_month_expense['amount'].sum()

        # Calculate the remaining budget
        remaining_budget = total_budget + total_expense  # Add because expenses are negative

        return {
            "Total Budget": total_budget,
            "Total Expense": total_expense,
            "Remaining Budget": remaining_budget
        }

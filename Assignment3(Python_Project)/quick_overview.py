# Importing required libraries
import pandas as pd
from datetime import datetime
import sys

# Class to get the current month overview
class QuickOverview:
    def __init__(self):
        # Read Expense, Income and Transaction data
        try:
            self.expense = pd.read_excel("./data/expense.xlsx")
            self.income = pd.read_excel("./data/income.xlsx")
            self.transaction = pd.read_excel("./data/transaction.xlsx")
            self.budget = pd.read_excel("./data/budgets.xlsx")
        # Error handling
        except PermissionError:
            print("Permission denied to read the file, please close the file before proceeding.")
            sys.exit(1)
        except FileNotFoundError:
            self.expense = pd.DataFrame(columns=["expenses_id", "date", "category", "description", "amount"])
            self.income = pd.DataFrame(columns=["income_id", "date", "category", "description", "amount"])
            self.transaction = pd.DataFrame(columns=["transaction_id", "date", "category", "description", "amount"])
            self.budgets = pd.DataFrame(columns=["transaction_id", "date", "category", "description", "amount"])

    def get_current_month_overview(self):
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Filter budget data for the current month and year
        self.income['date'] = pd.to_datetime(self.income['date'], errors='coerce')
        current_month_income = self.income[
            (self.income['date'].dt.month == current_month) & (self.income['date'].dt.year == current_year)
        ]
        total_income = current_month_income['amount'].sum()

        # Filter expense data for the current month and year
        self.expense['date'] = pd.to_datetime(self.expense['date'], errors='coerce')
        current_month_expense = self.expense[
            (self.expense['date'].dt.month == current_month) & (self.expense['date'].dt.year == current_year)
        ]
        total_expense = abs(current_month_expense['amount'].sum())

        return {
            "Total Income": total_income,
            "Total Expense": total_expense,
        }
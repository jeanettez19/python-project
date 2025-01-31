import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os,sys

class ExpenseAnalysis:
    def __init__(self, file_path):
        # Initialize by loading the Excel file and extracting sheets
        self.file_path = file_path
        self.data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets into a dictionary
        self.expense = self.data.get('expense', pd.DataFrame())
        self.budget = self.data.get('budget', pd.DataFrame())
        self.income = self.data.get('income', pd.DataFrame())
        self.transaction = self.data.get('transaction', pd.DataFrame())

        # Dynamically extract all unique categories across relevant sheets
        self.categories = pd.concat([
            self.budget['category'] if 'category' in self.budget else pd.Series(dtype='object'),
            self.expense['category'] if 'category' in self.expense else pd.Series(dtype='object')
        ]).dropna().sort_values().unique()

    def calculate_budgeted_vs_actual(self):
        # Sum up the budget and expense per category
        budgeted = self.budget.groupby('category')['monthly_budget'].sum() if not self.budget.empty else pd.Series(dtype='float')
        actual = self.expense.groupby('category')['amount'].sum() * -1 if not self.expense.empty else pd.Series(dtype='float')

        # Align both Series to the same categories
        self.budgeted, self.actual = budgeted.align(actual, fill_value=0)


    def calculate_total_budget_and_actual(self):
        # Calculate total budget and total actual
        self.total_budget = self.budgeted.sum() if not self.budgeted.empty else 0
        self.total_actual = self.actual.sum() if not self.actual.empty else 0

    def process_expense_data(self):
        # Parse dates for the expense DataFrame and extract month and day
        if not self.expense.empty:
            self.expense['date'] = pd.to_datetime(self.expense['date'], errors='coerce')
            self.expense['month'] = self.expense['date'].dt.to_period('M')
            self.expense['day'] = self.expense['date'].dt.date  # Add a 'day' column for daily tracking

    def calculate_monthly_expenses(self):
        # Monthly spending trends per category
        if not self.expense.empty:
            self.monthly_expenses = self.expense.groupby([self.expense['month'], 'category'])['amount'].sum().unstack().fillna(0)
        else:
            self.monthly_expenses = pd.DataFrame()

    def calculate_daily_expenses(self):
        # Daily spending trends per category
        if not self.expense.empty:
            self.daily_expenses = self.expense.groupby([self.expense['day'], 'category'])['amount'].sum().unstack().fillna(0)
        else:
            self.daily_expenses = pd.DataFrame()

    def calculate_daily_cumulative_sum(self):
        # Daily cumulative sum of spending per category
        if not self.daily_expenses.empty:
            self.daily_cumulative_sum = self.daily_expenses.cumsum()
        else:
            self.daily_cumulative_sum = pd.DataFrame()

    def calculate_daily_cumulative_sum_all_categories(self):
        # Calculate the cumulative sum for all categories combined (total daily cumulative)
        if not self.daily_expenses.empty:
            self.daily_cumulative_sum_all = self.daily_expenses.sum(axis=1).cumsum()
        else:
            self.daily_cumulative_sum_all = pd.Series(dtype='float')

    def calculate_daily_total_spending(self):
        # Calculate total daily spending (sum of all categories per day)
        if not self.daily_expenses.empty:
            self.daily_total_spending = self.daily_expenses.sum(axis=1)
        else:
            self.daily_total_spending = pd.Series(dtype='float')
# Importing required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Creating a class for our Insights
class Insights:
    # Initializing the class
    def __init__(self, expense_path, budget_path, income_path, transaction_path, category_path):
        # Importing data from each sheet
        self.expense = pd.read_excel(expense_path)
        self.budget = pd.read_excel(budget_path)
        self.income = pd.read_excel(income_path)
        self.transaction = pd.read_excel(transaction_path)
        self.category = pd.read_excel(category_path)

        # Data Manipulation for Expenses
        self.expense_positive = self.expense.copy()
        self.expense_positive['amount'] = self.expense_positive['amount'].abs()
        self.expense_positive['year_month'] = self.expense_positive['date'].dt.to_period('M')
        self.expense_positive['day'] = self.expense_positive['date'].dt.day
        self.actual = self.expense.groupby('category')['amount'].sum() * -1
        self.total_actual = self.actual.sum()

        # Data Manipulation for Budget
        self.budget['year_month'] = self.budget['date'].dt.to_period('M')
        self.budgeted = self.budget.groupby('category')['monthly_budget'].sum()
        self.total_budget = self.budgeted.sum()

    # Function to get the latest month
    def latest_month(self):
        self.latest_month = self.expense_positive['year_month'].max()
        latest_month_word = self.latest_month.strftime('%B %Y')
        self.expense_latest_month = self.expense_positive[self.expense_positive['year_month'] == self.latest_month]
        self.budget_latest_month = self.budget[self.budget['year_month'] == self.latest_month]
        return latest_month_word

    # Function to get the total expenses
    def expenses_by_category_latest_month(self):
        grouped_expense = self.expense_latest_month.groupby('category', as_index=False)['amount'].sum().sort_values(by='amount', ascending=False)
        return grouped_expense

    # Function to get the expenses vs budget by category
    def expense_vs_budget_by_category_latest_month(self):
        expense_by_category = self.expense_latest_month.groupby('category')['amount'].sum()
        budget_by_category = self.budget_latest_month.set_index('category')['monthly_budget']
        merged_by_category = pd.merge(expense_by_category, budget_by_category, on='category', how='outer')
        return merged_by_category

    # Function to get the daily expenses for the latest month
    def daily_expenses_latest_month(self):
        monthly_expenses = self.expense_latest_month.groupby([self.expense_latest_month['day'], 'category'])['amount'].sum().unstack().fillna(0)
        monthly_expenses = monthly_expenses.drop(columns=['Rent'], errors='ignore')
        return monthly_expenses

    # Function to get the expenses vs budget for the latest month
    def expenses_vs_budget_monthly(self):
        sum_expense = self.expense_positive.groupby(['year_month'])['amount'].sum()
        sum_budget = self.budget.groupby(['year_month'])['monthly_budget'].sum()
        budget_expense_df = pd.merge(sum_budget, sum_expense, on='year_month', how='outer')
        return budget_expense_df

    # Function to get the expenses by category for each month
    def expenses_by_category_monthly(self):
        monthly_spending = self.expense_positive.groupby(['year_month', 'category'])['amount'].sum().unstack()
        return monthly_spending
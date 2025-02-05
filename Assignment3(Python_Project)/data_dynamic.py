# Importing required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Creating a class for our Insights
class Insights:
    """
    This class does all the data manipulation such it can be reflected in the graphs clearly
    """
    # Initializing the class
    def __init__(self, expense_path, budget_path, income_path, transaction_path, category_path):
        self.load_data(expense_path, budget_path, income_path, transaction_path, category_path)

    # Function for all data processing
    def load_data(self, expense_path, budget_path, income_path, transaction_path, category_path):
        # Importing data sheets
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
        
        # Filtering out data for latest month for graphs 1, 2 and 3
        # Filtering out data for latest month for graphs 1, 2 and 3
        # Create the current month without setting a specific day
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.current_day = datetime.now().day
        self.current_month_timestamp = pd.Timestamp(year = self.current_year, month = self.current_month, day = self.current_day)
        current_month_year_month = self.current_month_timestamp.strftime('%Y-%m')
        current_month_word = self.current_month_timestamp.strftime('%B %Y')
        self.expense_latest_month = self.expense_positive[self.expense_positive['year_month'] == current_month_year_month]
        self.budget_latest_month = self.budget[self.budget['year_month'] == current_month_year_month]
        return current_month_word
  
    # Function for Graph 1, to display the expenses of each category in the latest month
    def expenses_by_category_latest_month(self): 
        grouped_expense = self.expense_latest_month.groupby('category', as_index=False)['amount'].sum().sort_values(by='amount', ascending=False)
        return grouped_expense

    # Function for graph 2, to get the expenses vs budget of each category in the latest month
    def expense_vs_budget_by_category_latest_month(self):
        expense_by_category = self.expense_latest_month.groupby('category')['amount'].sum()
        budget_by_category = self.budget_latest_month.set_index('category')['monthly_budget']
        merged_by_category = pd.merge(expense_by_category, budget_by_category, on='category', how='outer')
        return merged_by_category

    # Function for graph 3, to get the daily expenses everyday for the latest month
    def daily_expenses_latest_month(self):
        monthly_expenses = self.expense_latest_month.groupby([self.expense_latest_month['day'], 'category'])['amount'].sum().unstack().fillna(0)
        monthly_expenses = monthly_expenses.drop(columns=['Rent'], errors='ignore')
        return monthly_expenses

    # Function for graph 4, to get the expenses vs budget for all months
    def expenses_vs_budget_monthly(self):
        sum_expense = self.expense_positive.groupby(['year_month'])['amount'].sum()
        sum_budget = self.budget.groupby(['year_month'])['monthly_budget'].sum()
        budget_expense_df = pd.merge(sum_budget, sum_expense, on='year_month', how='outer')
        return budget_expense_df

    # Function for graph 5, to get the expenses of all categories for all month
    def expenses_by_category_monthly(self):
        monthly_spending = self.expense_positive.groupby(['year_month', 'category'])['amount'].sum().unstack()
        return monthly_spending
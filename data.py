import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os,sys

data = pd.read_excel('datagen.xlsx', sheet_name=['expense', 'budget', 'income', 'transaction'])

# Separate the sheets into individual DataFrames
expense = data['expense']
budget = data['budget']
income = data['income']
transaction = data['transaction']

# print(expense.head())
# print(budget.head())
# print(income.head())
# print(transaction.head())

categories = budget['category'].sort_values().unique()

# Sum up the budget and expense per category
budgeted = budget.groupby('category')['monthly_budget'].sum()
actual = expense.groupby('category')['amount'].sum() * -1

# Total budget and total actual
total_budget = budgeted.sum()
total_actual = actual.sum()
#print(total_actual)

# Spending Trends Over Time (assuming 'date' column exists in expense and budget)
# Parse dates for the expense DataFrame
expense['date'] = pd.to_datetime(expense['date'])
expense['month'] = expense['date'].dt.to_period('M')

# Monthly spending trends per category
monthly_expenses = expense.groupby([expense['month'], 'category'])['amount'].sum().unstack().fillna(0)

# Expense Breakdown by Category (Donut Chart)
expense_breakdown = actual

# Create the 2x2 matrix of graphs
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

# 1. Total Budget vs Actual (Pie Chart)
axes[0, 0].pie([total_budget, total_actual], labels=['Budgeted', 'Actual'], autopct='%1.1f%%', colors=['lightblue', 'salmon'], startangle=90, explode=(0.1, 0))
axes[0, 0].set_title('Total Budget vs Actual Expenses')

# 2. Budget vs Actual Comparison (Bar Chart)
axes[0, 1].bar(np.arange(len(categories)) - 0.35/2, budgeted, 0.35, label='Budgeted', color='skyblue')
axes[0, 1].bar(np.arange(len(categories)) + 0.35/2, actual, 0.35, label='Actual', color='salmon')
axes[0, 1].set_xlabel('Categories')
axes[0, 1].set_ylabel('Amount ($)')
axes[0, 1].set_title('Budget vs Actual Expenses')
axes[0, 1].set_xticks(np.arange(len(categories)))
axes[0, 1].set_xticklabels(categories)
axes[0, 1].legend()
# Tilt the x-axis labels by 45 degrees
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Expense Breakdown by Category (Donut Chart)
wedges, texts, autotexts = axes[1, 0].pie(expense_breakdown, labels=categories, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen', 'orange', 'salmon', 'yellow', 'purple'])
axes[1, 0].pie([1], radius=0.7, colors=['white'])  # Center hole to make it a donut chart

# Rotate the percentage labels
for autotext in autotexts:
    autotext.set_rotation(45)  # Rotate percentage labels by 45 degrees

axes[1, 0].set_title('Expense Breakdown by Category')

# 4. Spending Trends Over Time (Line Chart)
for category in categories:
    axes[1, 1].plot(monthly_expenses.index.astype(str), monthly_expenses[category] * -1, label=category, marker='o')

axes[1, 1].set_xlabel('Months')
axes[1, 1].set_ylabel('Amount ($)')
axes[1, 1].set_title('Spending Trends Over Time')
axes[1, 1].legend(loc='upper left', bbox_to_anchor=(1, 0), borderaxespad=0.5)

# Adjust the layout to make sure everything fits
plt.tight_layout()
plt.show()


class ExpenseAnalysis:
    def __init__(self, file_path):
        # Initialize by loading the Excel file and extracting sheets
        self.file_path = file_path
        self.data = pd.read_excel(file_path, sheet_name=['expense', 'budget', 'income', 'transaction'])
        self.expense = self.data['expense']
        self.budget = self.data['budget']
        self.income = self.data['income']
        self.transaction = self.data['transaction']

        # Extract unique categories from the budget
        self.categories = self.budget['category'].sort_values().unique()

    def display_data_head(self):
        # Display the first few rows of each DataFrame
        print(self.expense.head())
        print(self.budget.head())
        print(self.income.head())
        print(self.transaction.head())

    def calculate_budgeted_vs_actual(self):
        # Sum up the budget and expense per category
        self.budgeted = self.budget.groupby('category')['monthly_budget'].sum()
        self.actual = self.expense.groupby('category')['amount'].sum() * -1
        print(self.budgeted)

    def calculate_total_budget_and_actual(self):
        # Calculate total budget and total actual
        self.total_budget = self.budgeted.sum()
        self.total_actual = self.actual.sum()

    def process_expense_data(self):
        # Parse dates for the expense DataFrame and extract month
        self.expense['date'] = pd.to_datetime(self.expense['date'])
        self.expense['month'] = self.expense['date'].dt.to_period('M')
        self.expense['day'] = self.expense['date'].dt.date  # Add a 'day' column for daily tracking

    def calculate_monthly_expenses(self):
        # Monthly spending trends per category
        self.monthly_expenses = self.expense.groupby([self.expense['month'], 'category'])['amount'].sum().unstack().fillna(0)

    def calculate_daily_expenses(self):
        # Daily spending trends per category
        self.daily_expenses = self.expense.groupby([self.expense['day'], 'category'])['amount'].sum().unstack().fillna(0)

    def calculate_daily_cumulative_sum(self):
        # Daily cumulative sum of spending per category
        self.daily_cumulative_sum = self.daily_expenses.cumsum()

    def calculate_daily_cumulative_sum_all_categories(self):
        # Calculate the cumulative sum for all categories combined (total daily cumulative)
        self.daily_cumulative_sum_all = self.daily_expenses.sum(axis=1).cumsum()

    def calculate_daily_total_spending(self):
        # Calculate total daily spending (sum of all categories per day)
        self.daily_total_spending = self.daily_expenses.sum(axis=1)

    def plot_charts(self):
        # Ensure total_budget and total_actual are calculated
        self.calculate_total_budget_and_actual()

        # Create the 2x2 matrix of graphs
        fig, axes = plt.subplots(2, 2, figsize=(12, 12))

        # 1. Total Budget vs Actual (Pie Chart)
        axes[0, 0].pie([self.total_budget, self.total_actual], labels=['Budgeted', 'Actual'], autopct='%1.1f%%', colors=['lightblue', 'salmon'], startangle=90, explode=(0.1, 0))
        axes[0, 0].set_title('Total Budget vs Actual Expenses')

        # 2. Budget vs Actual Comparison (Bar Chart)
        axes[0, 1].bar(np.arange(len(self.categories)) - 0.35/2, self.budgeted, 0.35, label='Budgeted', color='skyblue')
        axes[0, 1].bar(np.arange(len(self.categories)) + 0.35/2, self.actual, 0.35, label='Actual', color='salmon')
        axes[0, 1].set_xlabel('Categories')
        axes[0, 1].set_ylabel('Amount ($)')
        axes[0, 1].set_title('Budget vs Actual Expenses')
        axes[0, 1].set_xticks(np.arange(len(self.categories)))
        axes[0, 1].set_xticklabels(self.categories)
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis='x', rotation=45)

        # 3. Expense Breakdown by Category (Donut Chart)
        expense_breakdown = self.actual
        wedges, texts, autotexts = axes[1, 0].pie(expense_breakdown, labels=self.categories, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen', 'orange', 'salmon', 'yellow', 'purple'])
        axes[1, 0].pie([1], radius=0.7, colors=['white'])  # Center hole to make it a donut chart

        # Rotate the percentage labels
        for autotext in autotexts:
            autotext.set_rotation(45)

        axes[1, 0].set_title('Expense Breakdown by Category')

        # 4. Spending Trends Over Time (Line Chart for Monthly, Daily, and Cumulative Trends)
        # # Plot Monthly Spending Trends
        # for category in self.categories:
        #     axes[1, 1].plot(self.monthly_expenses.index.astype(str), self.monthly_expenses[category] * -1, label=f'{category} (Monthly)', marker='o')

        # # Plot Daily Spending Trends
        # for category in self.categories:
        #     axes[1, 1].plot(self.daily_expenses.index.astype(str), self.daily_expenses[category] * -1, label=f'{category} (Daily)', linestyle='--')

        # # Plot Daily Cumulative Sum for Each Category
        # for category in self.categories:
        #     axes[1, 1].plot(self.daily_cumulative_sum.index.astype(str), self.daily_cumulative_sum[category] * -1, label=f'{category} (Cumulative)', linestyle='-.')

        # # Plot Combined Daily Cumulative Sum for All Categories
        # axes[1, 1].plot(self.daily_cumulative_sum_all.index.astype(str), self.daily_cumulative_sum_all * -1, label='All Categories (Cumulative)', linestyle='-', color='black', linewidth=2)

        # Plot Total Daily Spending (sum of all categories)
        axes[1, 1].plot(self.daily_total_spending.index.astype(str), self.daily_total_spending * -1, label='Total Daily Spending', linestyle='-', color='purple', linewidth=2)

        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Amount ($)')
        axes[1, 1].set_title('Spending Trends Over Time (Monthly, Daily, & Cumulative)')
        axes[1, 1].legend(loc='upper left', bbox_to_anchor=(1, 0), borderaxespad=0.5)

        # Adjust the layout to make sure everything fits
        plt.tight_layout()
        plt.show()

# Example usage:
file_path = 'datagen.xlsx'
analysis = ExpenseAnalysis(file_path)

# Display the first few rows of each DataFrame
analysis.display_data_head()

# Calculate and print budget vs actual values
analysis.calculate_budgeted_vs_actual()

# Process the expense data and calculate monthly, daily, and daily cumulative expenses
analysis.process_expense_data()
analysis.calculate_monthly_expenses()
analysis.calculate_daily_expenses()
analysis.calculate_daily_cumulative_sum()
analysis.calculate_daily_cumulative_sum_all_categories()  # New method to calculate total cumulative sum for all categories
analysis.calculate_daily_total_spending()  # New method to calculate total daily spending

# Plot the charts
analysis.plot_charts()


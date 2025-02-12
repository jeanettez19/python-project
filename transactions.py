import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os,sys
from category import Category

class Transaction:
    _id_counter = 1  # Default value if no data is loaded

    @classmethod
    def initialize_id_counter(cls, excel_file, id_column, extra_column = True):
        # Read the Excel file and find the maximum ID in the given column
        try:
            data = pd.read_excel(excel_file)
            max_id = data[id_column].max()
            cls._id_counter = max_id + 1 if not pd.isna(max_id) else 1
            print(cls._id_counter)

        except FileNotFoundError:
            print(f"{excel_file} does not exist... Creating new file")
            #data = pd.DataFrame(columns=[id_column, "Amount", "Date", "Description"])
            if extra_column == False:
                data = pd.DataFrame(columns=[id_column, "Date", "Category", "Description", "Amount"])

            else:
                data = pd.DataFrame(columns=[id_column, "Date", "Category", "Description", "Amount", "Transaction ID"])
            data.to_excel(excel_file, index=False)
            cls._id_counter = 1  # Fallback if file not found

        except PermissionError:
            print(f"Permission denied to read {excel_file}, please close the file before proceeding.")
            sys.exit(1)

        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

        return data

    def __init__(self, transaction_date, transaction_category, transaction_description, transaction_amount):
        self.transaction_id = Transaction._id_counter
        self.transaction_amount = transaction_amount
        self.transaction_date = transaction_date
        self.transaction_description = transaction_description
        self.transaction_category = transaction_category

    def display_info(self):
        print(f"Transaction ID:{self.transaction_id}, Date:{self.transaction_date}, Category:{self.transaction_category}" +
        f"Description:{self.transaction_description}, Amount:{self.transaction_amount}")

    def save_file_to_excel(excel_file, existing_data, transactions, type):
        try:
            # Prepare new data
            if type == "transactions":
                new_data = pd.DataFrame(
                    [{"transaction_id": transaction.transaction_id, "date": transaction.transaction_date,
                      "category": transaction.transaction_category, "description": transaction.transaction_description,
                      "amount": transaction.transaction_amount} for transaction in transactions])

            elif type == "expenses"    :
                new_data = pd.DataFrame(
                    [{"expenses_id": expense.expenses_id, "date": expense.transaction_date,
                      "category": expense.transaction_category, "description": expense.transaction_description,
                      "amount": expense.transaction_amount, "transaction_id": expense.transaction_id} for expense in transactions])

            elif type == "income":
                new_data = pd.DataFrame(
                    [{"income_id": income.income_id, "date": income.transaction_date,
                      "category": income.transaction_category, "description": income.transaction_description,
                      "amount": income.transaction_amount, "transaction_id": income.transaction_id} for income in transactions])

            # Append new data to existing data
            if existing_data.empty:
                updated_data = new_data
            else:
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            # Save back to Excel
            updated_data.to_excel(excel_file, index=False)
            print(f"Transactions saved")
        except Exception as e:
            print(f"Error saving to Excel: {e}")

    def add_transaction(transaction_word):
        cat = Category.initialize('./data/Categories.xlsx')
        print(f"\nEnter {transaction_word} details:")
        try:
            while True:
                date = input("Transaction Date (DD-MM-YYYY) :")
                current_date = datetime.now()
                try:
                    datetime.strptime(date, "%d-%m-%Y")
                    if datetime.strptime(date, "%d-%m-%Y") < current_date:
                      break
                    else:
                       print("Date entered is in the future. Please enter a valid date\n")
                except ValueError:
                    print("Invalid date format. Please enter the date in DD-MM-YYYY format\n")

            while True:
                cat.display_info()
                cat_id = int(input("\nSelect the category_id:"))
                category_name = cat.get_category(cat_id)
                break

            description = input(f"\n{transaction_word} Description: ")

            while True:
                try:
                    amount = float(input(f"\n{transaction_word} Amount: "))
                    if amount <= 0:
                        print("Amount must be greater than 0. Please enter amount again\n")
                    elif len(str(amount).split(".")[1]) > 2:
                          print("Amount can have at most two decimal places. Please enter amount again\n")
                    else:
                        break
                except ValueError:
                    print("invalid input. PLease enter numeric values\n")

            transaction_file = Transaction.initialize_id_counter("./data/transaction.xlsx","transaction_id", False)
            # Create a new transaction
            if transaction_word == "Income":
                income_file = Income.initialize_id_counter("./data/income.xlsx", "income_id")
                new_transaction = Income(date, category_name, description, amount)
                Income.save_file_to_excel("./data/income.xlsx", income_file,[new_transaction], "income")

            elif transaction_word == "Expenses":
                expenses_file = Expenses.initialize_id_counter("./data/expense.xlsx", "expenses_id")
                amount = -amount
                new_transaction = Expenses(date, category_name, description, amount)
                Expenses.save_file_to_excel("./data/expense.xlsx", expenses_file,[new_transaction], "expenses")

            Transaction.save_file_to_excel("./data/transaction.xlsx", transaction_file,[new_transaction], "transactions")
            print(f"\n{transaction_word} added successfully:")
            new_transaction.display_info()  # Display the transaction details
        except Exception as e:
            print(f"An error occurred: {e}")

    def remove_transaction(transaction_word):
        if transaction_word == "Expenses":
            try:
                expenses_data = pd.read_excel("./data/expense.xlsx")
                total_rows = len(expenses_data)
                start_index = max(0, total_rows - 10)

                while True:
                    print(expenses_data.iloc[start_index:total_rows])
                    
                    # Check if there are earlier rows
                    if start_index == 0:
                        print("\nNo more rows to display.")
                        #break
                    print("Enter 'n' to view earlier 10 entries")
                    print("Enter '0' to exit")
                    print("Enter the Income ID of the entry to remove it")
                    next_action = input("Enter your choice: ").strip().lower()

                    if next_action == 'n':
                            # Update the indices to show the previous 10 rows
                        total_rows = start_index
                        start_index = max(0, start_index - 10)

                    elif next_action == '0':
                        break

                    elif next_action.isdigit() and int(next_action) != 0:
                        row_number = int(next_action)
                        if row_number in expenses_data["expenses_id"].values:
                            expenses_data = expenses_data[expenses_data["expenses_id"] != row_number]
                            expenses_data.to_excel("./data/expense.xlsx", index = False)
                            print (f"Entry with Expense ID {row_number} has been removed.")
                            break
                        else:
                            print (f"Expense ID {row_number} not found. Please enter a valid Expense ID")
                    else:
                        print("Invalid selection. Choose 'n' to view previous 10 rows, or '0' to exit")
            except Exception as e:
                    print(f"Error: {e}")   
        elif transaction_word == 'Income':
            try:
                income_data = pd.read_excel("./data/income.xlsx")
                total_rows = len(income_data)
                start_index = max(0, total_rows - 10)

                while True:
                    print(income_data.iloc[start_index:total_rows])
                    
                    # Check if there are earlier rows
                    if start_index == 0:
                        print("\nNo more rows to display.")
                        #break
                    print("Enter 'n' to view earlier 10 entries")
                    print("Enter '0' to exit")
                    print("Enter the Income ID of the entry to remove it")
                    next_action = input("Enter your choice: ").strip().lower()

                    if next_action == 'n':
                            # Update the indices to show the previous 10 rows
                        total_rows = start_index
                        start_index = max(0, start_index - 10)

                    elif next_action == '0':
                        break

                    elif next_action.isdigit() and int(next_action) != 0:
                        row_number = int(next_action)
                        if row_number in income_data["income_id"].values:
                            income_data = income_data[income_data["income_id"] != row_number]
                            income_data.to_excel("./data/income.xlsx", index = False)
                            print (f"Entry with Income ID {row_number} has been removed.")
                            break
                        else:
                            print (f"Income ID {row_number} not found. Please enter a valid Income ID")
                    else:
                        print("Invalid selection. Choose 'n' to view previous 10 rows, or '0' to exit")
            except Exception as e:
                    print(f"Error: {e}")

class Expenses(Transaction):
    _id_counter = 1

    def __init__(self, transaction_date, transaction_category, transaction_description, transaction_amount):
        super().__init__(transaction_date, transaction_category, transaction_description, transaction_amount)
        self.expenses_id = Expenses._id_counter
        Expenses._id_counter += 1
        self.transaction_id = Transaction._id_counter
        Transaction._id_counter += 1

    def display_info(self):
        print(f"Expenses ID:{self.expenses_id}, Date:{self.transaction_date}, " +
              f"Category:{self.transaction_category}, Description:{self.transaction_description}, Amount:{self.transaction_amount}")
        
class Income(Transaction):
    _id_counter = 1

    def __init__(self,transaction_date, transaction_category, transaction_description, transaction_amount):
        super().__init__(transaction_date, transaction_category, transaction_description, transaction_amount)
        self.transaction_id = Transaction._id_counter
        self.income_id = Income._id_counter
        Income._id_counter += 1
        Transaction._id_counter += 1

    def display_info(self):
        print(f"Income ID:{self.income_id}, Date:{self.transaction_date}, Category:{self.transaction_category}," +
              f" Description:{self.transaction_description}, Amount:{self.transaction_amount}")        

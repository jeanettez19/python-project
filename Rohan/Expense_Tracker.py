# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime
from transactions import Transaction, Expenses
import os
import pandas as pd


class ExpenseTracker:
    
    # Creating a function to open a new window (Expense Tracker)
    def open_window(self):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            window = Toplevel(self)
            window.title("Expense Tracker")
            window.geometry("600x400")

            # Top Labels for the window
            top_f = Frame(window)
            top_f.pack(fill=X, padx=3, pady=3)

            back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
            back_button.pack(side=LEFT)

            # Sample data for table display purooses

            expenses_data = Expenses.initialize_id_counter(current_directory + "/data/expense.xlsx", "expenses_id")
            expenses_data["date"] = pd.to_datetime(expenses_data["date"])
            expenses_data = expenses_data.sort_values(by=["date", "expenses_id"], ascending=True)
            expenses_data["date"] = expenses_data["date"].dt.strftime("%d-%m-%Y")
            data = expenses_data.drop(columns=["expenses_id", "transaction_id"]).to_dict(orient="records")
            # Table for the entries
            table_frame = Frame(window)
            table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

            columns = ('Category','Description',"Amount", "Date")
            tree = Treeview(table_frame, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(fill=BOTH, expand=True)

            # Page variables
            rows_per_page = 15

            # Declaring a global variable for the current page
            global curr_page
            curr_page = 1


            # Function to display the table content
            def display_table(page):
                # Clear the Treeview
                for row in tree.get_children():
                    tree.delete(row)

                # Calculate the data to display on the current page
                start_index = (page - 1) * rows_per_page
                end_index = start_index + rows_per_page
                page_data = data[start_index:end_index]

                # Insert rows into the Treeview
                for entry in page_data:
                    tree.insert("", "end", values=(entry["category"], entry["description"] ,entry["amount"], entry["date"]))

                # Enable or disable Checkbuttons based on the current page
                if page == 1:
                    prev_checkbutton.config(state=DISABLED)
                else:
                    prev_checkbutton.config(state=NORMAL)

                if page >= len(data) / rows_per_page:
                    next_checkbutton.config(state=DISABLED)
                else:
                    next_checkbutton.config(state=NORMAL)

            # Function for the Previous button
            def previous_page():
                global curr_page  # Declare as global
                curr_page = curr_page - 1
                display_table(curr_page)

            # Function for the Next button
            def next_page():
                global curr_page  # Declare as global
                curr_page = curr_page + 1
                display_table(curr_page)

            # Display the bottom buttons
            bottom_f = Frame(window)
            bottom_f.pack(fill=X, padx=5, pady=5)

            prev_checkbutton = Button(window, text="Previous", command=previous_page)
            prev_checkbutton.pack(side=LEFT, padx=5)

            next_checkbutton = Button(window, text="Next", command=next_page)
            next_checkbutton.pack(side=LEFT, padx=5)

            # Initial table display
            display_table(curr_page)


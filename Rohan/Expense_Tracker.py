# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime


class ExpenseTracker:
    
    # Creating a function to open a new window (Expense Tracker)
    def open_window(self):
            window = Toplevel(self)
            window.title("Expense Tracker")
            window.geometry("600x400")

            # Top Labels for the window
            top_f = Frame(window)
            top_f.pack(fill=X, padx=3, pady=3)

            back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
            back_button.pack(side=LEFT)

            # Sample data for table display purooses
            data = [
                {"Category": "Food", "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-01"},
                {"Category": "Transport",  "Description": "I hate myself" ,"Amount": 20, "Date": "2025-01-02"},
                {"Category": "Groceries",  "Description": "I hate myself" ,"Amount": 100, "Date": "2025-01-03"},
                {"Category": "Entertainment",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-04"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 200, "Date": "2025-01-05"},
                {"Category": "Travel",  "Description": "I hate myself" ,"Amount": 150, "Date": "2025-01-06"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 30, "Date": "2025-01-07"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-08"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-09"},
                {"Category": "Travel",  "Description": "I hate myself" ,"Amount": 670, "Date": "2025-01-09"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 33, "Date": "2025-01-10"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 624, "Date": "2025-01-10"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 34, "Date": "2025-01-10"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 56, "Date": "2025-01-10"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 12, "Date": "2025-01-10"},
                {"Category": "Entertainment",  "Description": "I hate myself" ,"Amount": 356, "Date": "2025-01-10"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 123, "Date": "2025-01-11"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 44, "Date": "2025-01-12"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 64, "Date": "2025-01-12"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 6, "Date": "2025-01-13"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-13"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-14"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-14"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-14"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 680, "Date": "2025-01-15"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 80, "Date": "2025-01-15"},
                {"Category": "Groceries",  "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-15"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-15"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-16"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 680, "Date": "2025-01-16"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 80, "Date": "2025-01-16"},
                {"Category": "Groceries",  "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-17"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-17"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-17"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 680, "Date": "2025-01-17"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 80, "Date": "2025-01-17"},
                {"Category": "Groceries",  "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-17"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 40, "Date": "2025-01-18"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 60, "Date": "2025-01-18"},
                {"Category": "Bills",  "Description": "I hate myself" ,"Amount": 680, "Date": "2025-01-18"},
                {"Category": "Medical",  "Description": "I hate myself" ,"Amount": 80, "Date": "2025-01-19"},
                {"Category": "Groceries",  "Description": "I hate myself" ,"Amount": 50, "Date": "2025-01-19"},
                {"Category": "Clothing",  "Description": "I hate myself" ,"Amount": 20, "Date": "2025-01-19"},
                {"Category": "Food",  "Description": "I hate myself" ,"Amount": 10, "Date": "2025-01-19"},
                {"Category": "Joaquin's Services",  "Description": "I hate myself" ,"Amount": 1, "Date": "2025-01-27"}
            ]

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
                    tree.insert("", "end", values=(entry["Category"], entry["Description"] ,entry["Amount"], entry["Date"]))

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


# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from datetime import datetime

# Import Backend file
from backend_budget import Budget


class Budgets:
    def open_BSwindow(self):
            # Creating a new window
            window = Toplevel(self)
            window.title("Budget")
            window.geometry("810x400")

            # Top Labels for the window
            top_f = Frame(window)
            top_f.pack(fill=X, padx=5, pady=5)

            back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
            back_button.pack(side=LEFT)


            # Table for the entries
            table_frame = Frame(window)
            table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

            columns = ('Category',"Amount", "Date")
            tree = Treeview(table_frame, columns=columns, show="headings")
            
            
            budget_data = Budget().initialize("./data/budgets.xlsx", "./data/categories.xlsx")
            budget_data = budget_data.get_all_budgets()
            print(budget_data)
            for budget in budget_data:
                tree.insert("", "end", values=(budget['category'], f"{budget['monthly_budget']:.2f}", budget['date']))
                

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(fill=BOTH, expand=True)


            input_frame = Frame(window)
            input_frame.pack(fill=X, padx=5, pady=5)

            # Replace the DateEntry with these two Combobox widgets
            months = [ "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December" ]
            years = [str(year) for year in range(2000, datetime.now().year + 11)]

            category_entryB = Entry(input_frame)
            category_entryB.pack(side=LEFT, fill=X, expand=True, padx=2)
            category_entryB.insert(0, "Category")

            amount_entryB = Entry(input_frame)
            amount_entryB.pack(side=LEFT, fill=X, expand=True, padx=2)
            amount_entryB.insert(0, "(SGD)")

            month_combobox = ttk.Combobox(input_frame, values=months, width=10)
            month_combobox.set("Month")
            month_combobox.pack(side=LEFT, fill=X, expand=True, padx=2)

            year_combobox = ttk.Combobox(input_frame, values=years, width=6)
            year_combobox.set("Year")
            year_combobox.pack(side=LEFT, fill=X, expand=True, padx=2)

            def add_to_table():
                category = category_entryB.get()
                amount = amount_entryB.get()
                month = month_combobox.get()
                year = year_combobox.get()

                # Validate amount
                try:
                    amount = float(amount)
                    if amount < 0:
                        messagebox.showerror("Invalid Input", "Amount cannot be negative.")
                        return
                    amount = round(amount, 2)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Amount must be a number greater than 0.")
                    return None

                # Validate month and year
                if month == "Month" or year == "Year":
                    messagebox.showerror("Invalid Input", "Please select both month and year.")
                    return

                date = f"{month}-{year}"  # Format as Month-Year

                if category and amount and date:
                    tree.insert("", "end", values=(category, f"{amount:.2f}", date))
                    category_entryB.delete(0, END)
                    amount_entryB.delete(0, END)
                    month_combobox.set("Month")
                    year_combobox.set("Year")
                
            add_button = Button(input_frame, text="Add", bg="gray", command=add_to_table)
            add_button.pack(side=LEFT, padx=5)

            # Bottom buttons
            bottom_frame = Frame(window)
            bottom_frame.pack(fill=X, padx=5, pady=5)

            remove_button = Button(bottom_frame, text="Remove", bg="orange")
            remove_button.pack(side=LEFT, padx=2)
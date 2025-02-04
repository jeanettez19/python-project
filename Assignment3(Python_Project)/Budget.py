# Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from datetime import datetime

# Import Backend file
from backend_budget import Budget
from backend_category import Category

# Creating a class for our Budgets window
class Budgets:
    def open_bs_window(self):
        # Creating a new window
        cat_class = Category().initialize("./data/categories.xlsx")
        window = Toplevel(self)
        window.title("Budget")
        window.geometry("810x400")

        # Top Labels for the BS window
        top_f = Frame(window)
        top_f.pack(fill=X, padx=5, pady=5)

        back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Table for the entries
        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Columns of the table
        columns = ('budget_id', 'Category', "Amount", "Date")
        tree = Treeview(table_frame, columns=columns, show="headings")

        budget_class = Budget().initialize("./data/budgets.xlsx", "./data/categories.xlsx")
        budget_data = budget_class.get_all_budgets()
        for budget in budget_data:
            tree.insert("", "end", values=(budget['budget_id'], budget['category'], f"{budget['monthly_budget']:.2f}", budget['date']))

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=BOTH, expand=True)

        input_frame = Frame(window)
        input_frame.pack(fill=X, padx=5, pady=5)

        # Months for the combobox
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        # Years for the combobox
        years = [str(year) for year in range(2000, datetime.now().year + 11)]

        categories_all = cat_class.get_all_categories()

        # Retrieve only expense items
        expense_items = [category['category_name'] for category in categories_all if category.get('category_type') == "Expenses"]

        # Create a StringVar for the category dropdown
        category_entryB = ttk.Combobox(input_frame, values=expense_items, width=20)
        category_entryB.pack(side=LEFT, fill=X, expand=True, padx=2)
        category_entryB.insert(0, "Category")

        # Create a StringVar for the amount entry
        amount_entryB = Entry(input_frame)
        amount_entryB.pack(side=LEFT, fill=X, expand=True, padx=2)
        amount_entryB.insert(0, "(SGD)")

        # Create a Combobox for the month and year
        month_combobox = ttk.Combobox(input_frame, values=months, width=10)
        month_combobox.set("Month")
        month_combobox.pack(side=LEFT, fill=X, expand=True, padx=2)

        year_combobox = ttk.Combobox(input_frame, values=years, width=6)
        year_combobox.set("Year")
        year_combobox.pack(side=LEFT, fill=X, expand=True, padx=2)

        # Function to refresh the table
        def refresh_table():
            # Clear existing entries
            for item in tree.get_children():
                tree.delete(item)

            # Fetch updated data
            budget_data = budget_class.get_all_budgets()

            # Re-insert updated data
            for budget in budget_data:
                tree.insert("", "end", values=(budget['budget_id'], budget['category'], f"{budget['monthly_budget']:.2f}", budget['date']))

        # Function to add to the table
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
            elif month != months and year != years:
                messagebox.showerror("Invalid Input", "Please select valid month and year.")
                return

            # Convert month to month number
            month = months.index(month) + 1
            # Format date as the first day of month-year
            date = f"01-{month}-{year}"

            # Insert inputs into table once everything is valid
            if category and amount and date:
                tree.insert("", "end", values=(category, f"{amount:.2f}", date))
                category_entryB.delete(0, END)
                amount_entryB.delete(0, END)
                month_combobox.set("Month")
                year_combobox.set("Year")
            category_id = cat_class.get_category_id_by_name(category)
            budget_class.create_budget(date, category_id, amount)
            refresh_table()

        # Function to remove the selected item from the table
        def remove_from_table():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a row to delete.")
                return

            # Get the budget_id of the selected row
            budget_id = tree.item(selected)['values'][0]
            for selection in selected:
                tree.delete(selection)
            budget_class.delete_budget(budget_id)

        add_button = Button(input_frame, text="Add", bg="gray", command=add_to_table)
        add_button.pack(side=LEFT, padx=5)

        # Bottom buttons
        bottom_frame = Frame(window)
        bottom_frame.pack(fill=X, padx=5, pady=5)

        remove_button = Button(bottom_frame, text="Remove", bg="orange", command=remove_from_table)
        remove_button.pack(side=LEFT, padx=2)
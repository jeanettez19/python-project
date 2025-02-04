# Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from datetime import datetime

# Import Backend file
from backend_transactions import Transaction, Income, Expenses
from backend_category import Category

# Creating a class for our Financial Entries Window
class FinancialEntries:
    def open_fe_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Financial Entries")
        window.geometry("810x400")

        # Top Labels for the FE window
        top_f = Frame(window)
        top_f.pack(fill=X, padx=5, pady=5)

        back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Table for the entries
        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Columns of the table
        columns = ("Type", 'Category', 'Description', "Amount", "Date")
        tree = Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=BOTH, expand=True)

        # Data
        options = ["Expenses", "Income"]
        cat = Category().initialize("./data/categories.xlsx")
        categories_all = cat.get_all_categories()
        
        # Retrieve only expense items
        expense_items = [category['category_name'] for category in categories_all if category.get('category_type') == "Expenses"]
        income_items = [category['category_name'] for category in categories_all if category.get('category_type') == "Income"]

        # Create a StringVar for the category dropdown
        cat_var = StringVar()

        # Create a StringVar for the dynamic items dropdown
        item_var = StringVar()

        # Function to update the dropdown based on the selected category
        def update_dropdown(*args):
            selected_category = cat_var.get()
            if selected_category == "Expenses":
                item_var.set('')
                name_entry['values'] = expense_items
            elif selected_category == "Income":
                item_var.set('')
                name_entry['values'] = income_items
            else:
                item_var.set('')
                name_entry['values'] = expense_items

        # Input fields
        input_frame = Frame(window)
        input_frame.pack(fill=X, padx=5, pady=5)

        # Two Combobox widgets for Type and Category
        options = ["Expenses", "Income"]
        type_entry = ttk.Combobox(input_frame, values=options, state="readonly", textvariable=cat_var)
        type_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        type_entry.set("(Expenses / Income)")

        # Combobox for Category
        name_entry = ttk.Combobox(input_frame, textvariable=item_var)
        name_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        name_entry.set("(Category)")

        # Trace the changes in the type_entry
        cat_var.trace_add('write', update_dropdown)

        # Entry widgets for Description and Amount
        description_entry = Entry(input_frame)
        description_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        description_entry.insert(0, "Description")

        amount_entry = Entry(input_frame)
        amount_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        amount_entry.insert(0, "(SGD)")

        # DateEntry widget for Date
        date_entry = DateEntry(
            input_frame,
            width=15,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="MM-DD-YYYY",  # Format: Year-Month-Day
        )
        date_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
        date_entry.insert(0, "")

        # Function to get the data from the table
        def get_tree_data():
            data = []
            for item in tree.get_children():
                data.append(tree.item(item)['values'])
            print(data)
            return data

        # Function to save the data to the excel file
        def save_to_excel():
            obj = get_tree_data()
            for item in obj:
                type = item[0]
                name = item[1]
                description = item[2]
                amount = round(float(item[3]), 2)
                date = datetime.strptime(item[4], "%m-%d-%Y")

                # add through the backend Transaction class
                transaction_file = Transaction.initialize_id_counter("./data/transaction.xlsx", "transaction_id", False)
                if type == "Income":
                    income_file = Income.initialize_id_counter("./data/income.xlsx", "income_id")
                    new_transaction = Income(date, name, description, amount)
                    Income.save_file_to_excel("./data/income.xlsx", income_file, [new_transaction], "income")

                elif type == "Expenses":
                    expenses_file = Expenses.initialize_id_counter("./data/expense.xlsx", "expenses_id")
                    amount = -amount
                    new_transaction = Expenses(date, name, description, amount)
                    Expenses.save_file_to_excel("./data/expense.xlsx", expenses_file, [new_transaction], "expenses")

                Transaction.save_file_to_excel("./data/transaction.xlsx", transaction_file, [new_transaction], "transactions")

        # Function to remove the selected item from the table
        def remove_from_table():
            selected = tree.selection()
            for item in selected:
                tree.delete(item)

        # Function to add the data to the table
        def add_to_table():
            type = type_entry.get()
            name = name_entry.get()
            description = description_entry.get()
            amount = amount_entry.get()
            date = date_entry.get()

            # Validate Type
            if type not in ["Expenses", "Income"]:
                messagebox.showerror("Invalid Input", "Please enter 'Expenses' or 'Income' in the description field.")
                return

            # Validate Amount
            try:
                amount = float(amount)
                if amount < 0:
                    messagebox.showerror("Invalid Input", "Amount cannot be negative.")
                    return
                amount = round(amount, 2)
            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a number greater than 0.")
                return None

            # Validate Date
            try:
                datetime.strptime(date, "%m-%d-%Y")
            except ValueError:
                messagebox.showerror("Invalid Input", "Date must be in MM-DD-YYYY format.")
                return

            # Insert inputs into table once everything is valid
            if type and name and description and amount and date:
                tree.insert("", "end", values=(type, name, description, f"{amount:.2f}", date))
                type_entry.delete(0, END)
                name_entry.delete(0, END)
                description_entry.delete(0, END)
                amount_entry.delete(0, END)
                date_entry.delete(0, END)

        add_button = Button(input_frame, text="Add", bg="gray", command=add_to_table)
        add_button.pack(side=LEFT, padx=5)

        # Bottom buttons
        bottom_frame = Frame(window)
        bottom_frame.pack(fill=X, padx=5, pady=5)

        remove_button = Button(bottom_frame, text="Remove", bg="orange", command=remove_from_table)
        remove_button.pack(side=LEFT, padx=2)

        save_button = Button(bottom_frame, text="Save", bg="green", command=save_to_excel)
        save_button.pack(side=LEFT, padx=2)
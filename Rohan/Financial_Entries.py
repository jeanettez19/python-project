# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from datetime import datetime


class FinancialEntries:

    def open_FEwindow(self):

            # Creating a new window
            window = Toplevel(self)
            window.title("Financial Entries")
            window.geometry("810x400")

            # Top Labels for the window
            top_f = Frame(window)
            top_f.pack(fill=X, padx=5, pady=5)

            back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
            back_button.pack(side=LEFT)


            # Table for the entries
            table_frame = Frame(window)
            table_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

            columns = ("Type",'Category','Description',"Amount", "Date")
            tree = Treeview(table_frame, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            tree.pack(fill=BOTH, expand=True)

            def update_dropdown(*args):
                selected_category = cat_var.get()
                if selected_category == "Expense":
                    item_var.set('')
                    name_entry['values'] = expense_items
                elif selected_category == "Income":
                    item_var.set('')
                    name_entry['values'] = income_items
                else:
                    item_var.set('')
                    name_entry['values'] = []

            # Sample data
            options = ["Expense", "Income"]
            expense_items = ["Rent", "Utilities", "Groceries"]
            income_items = ["Salary", "Bonus", "Investments"]


            # Create a StringVar for the category dropdown
            cat_var = StringVar()
            cat_var.trace('w', update_dropdown)

            # Create a StringVar for the dynamic dropdown
            item_var = StringVar()

            # Input fields
            input_frame = Frame(window)
            input_frame.pack(fill=X, padx=5, pady=5)


            options = ["Expense", "Income"]
            type_entry = ttk.Combobox(input_frame, values=options, state="readonly", textvariable=cat_var)
            type_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
            type_entry.set("(Expense / Income)")

            name_entry = ttk.Combobox(input_frame,textvariable=item_var)
            name_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
            name_entry.set("(Cateogy)")

            description_entry = Entry(input_frame)
            description_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
            description_entry.insert(0, "Description")

            amount_entry = Entry(input_frame)
            amount_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
            amount_entry.insert(0, "(SGD)")

            date_entry = DateEntry(
            input_frame,
            width=15,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="MM-DD-YYYY",  # Format: Year-Month-Day)
            )
            date_entry.pack(side=LEFT, fill=X, expand=True, padx=2)
            date_entry.insert(0, "")

            def add_to_table():
                type = type_entry.get()
                name = name_entry.get()
                description = description_entry.get()
                amount = amount_entry.get()
                date = date_entry.get()

                # Validate Type
                if type not in ["Expense", "Income"]:
                    messagebox.showerror("Invalid Input", "Please enter 'Expense' or 'Income' in the description field.")
                    return

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

                # Validate date format
                try:
                    datetime.strptime(date, "%m-%d-%Y")
                except ValueError:
                    messagebox.showerror("Invalid Input","Date must be in MM-DD-YYYY format.")
                    return


                if type and name and description and amount and date:
                    tree.insert("", "end", values=(type, name, description,f"{amount:.2f}", date))
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

            remove_button = Button(bottom_frame, text="Remove", bg="orange")
            remove_button.pack(side=LEFT, padx=2)

            edit_button = Button(bottom_frame, text="Edit", bg="gray")
            edit_button.pack(side=LEFT, padx=2)
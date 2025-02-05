# Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Importing Functions from other Files
from budget import Budgets
from my_finances import MyFinances
from financial_entries import FinancialEntries
from expense_tracker import ExpenseTracker
from quick_overview import QuickOverview

# Creating a class for our Main Window
class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Setting the title of our main window
        self.title("Budget and Expense Tracker")
        self.geometry("500x450")

        # Creating a frame for our main window
        frame = LabelFrame(
            self,
            text="Welcome to Group 3's Budget and Expense Tracker",
            padx=30,
            pady=30,
            font=("Arial", 12)
        )
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Creating buttons for our main window
        self.button1 = Button(
            frame, text="Financial Entries",
            command=lambda: FinancialEntries.open_fe_window(self),
            font=("Arial", 12), fg="black"
        )
        self.button1.pack(pady=10)

        self.button2 = Button(
            frame, text="Expense Tracker",
            command=lambda: ExpenseTracker.open_window(self),
            font=("Arial", 12), fg="black"
        )
        self.button2.pack(pady=10)

        self.button3 = Button(
            frame, text="Set Budget",
            command=lambda: Budgets.open_bs_window(self),
            font=("Arial", 12), fg="black"
        )
        self.button3.pack(pady=10)

        self.button4 = Button(
            frame, text="My Finances",
            command=lambda: MyFinances.open_mf_window(self),
            font=("Arial", 12), fg="black"
        )
        self.button4.pack(pady=10)

        # Bottom frame for overview labels
        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(side=BOTTOM, fill="x")

        # Overview labels
        self.income_label = Label(self.bottom_frame, text="", font=("Arial", 12))
        self.income_label.pack()
        
        self.expense_label = Label(self.bottom_frame, text="", font=("Arial", 12))
        self.expense_label.pack()
        
        self.budget_label = Label(self.bottom_frame, text="", font=("Arial", 12))
        self.budget_label.pack()

        # Call the update method every 3 seconds
        self.update_overview()

    def update_overview(self):
        """Fetches new overview data and updates the labels every 3 seconds."""
        overview = QuickOverview()
        result = overview.get_current_month_overview()

        # Update label texts
        self.income_label.config(text=f"Income This Month: ${result['Total Income']:.2f}")
        self.expense_label.config(text=f"Expenses This Month: ${result['Total Expense']:.2f}")
        self.budget_label.config(text=f"Total Budget This Month: ${result['Total Budget']:.2f}")

        # Schedule next update in 3 seconds (3000 milliseconds)
        self.after(3000, self.update_overview)

# Run the application
MainWindow().mainloop()

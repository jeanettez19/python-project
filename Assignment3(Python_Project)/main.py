# Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime

# Importing Functions from other Files
from Expense_Tracker import ExpenseTracker
from quick_overview import QuickOverview

# Creating a class for our Main Window
class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Setting the title of our main window
        self.title("Budget and Expense Tracker")
        self.geometry("500x350")

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
        # Financial Entries Button
        self.button1 = Button(
            frame,
            text="Financial Entries",
            command=lambda: FinancialEntries.open_fe_window(self),
            font=("Arial", 12),
            fg="black"
        )
        self.button1.pack(pady=10)

        # Expense Tracker Button
        self.button2 = Button(
            frame,
            text="Expense Tracker",
            command=lambda: ExpenseTracker.open_window(self),
            font=("Arial", 12),
            fg="black"
        )
        self.button2.pack(pady=10)

        # Budgets Button
        self.button3 = Button(
            frame,
            text="Set Budget",
            command=lambda: Budgets.open_bs_window(self),
            font=("Arial", 12),
            fg="black"
        )
        self.button3.pack(pady=10)

        # My Finances Button
        self.button4 = Button(
            frame,
            text="My Finances",
            command=lambda: MyFinances.open_mf_window(self),
            font=("Arial", 12),
            fg="black"
        )
        self.button4.pack(pady=10)

        # Creating a label for the bottom of the main window
        overview = QuickOverview()
        result = overview.get_current_month_overview()
        Label(
            self,
            text=f"Budget Left This Month: ${result['Total Income']:.2f}",
            font=("Arial", 12)
        ).pack(side=BOTTOM)
        Label(
            self,
            text=f"Expenses This Month: ${result['Total Expense']:.2f}",
            font=("Arial", 12)
        ).pack(side=BOTTOM)

MainWindow().mainloop()

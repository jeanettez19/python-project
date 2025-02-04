# Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime
from data_dynamic import Insights
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Creating an instance of the Insights class
analysis = Insights(
    "./data/expense.xlsx",
    "./data/budgets.xlsx",
    "./data/income.xlsx",
    "./data/transaction.xlsx",
    "./data/categories.xlsx"
)

# Getting the latest month
latest_month = analysis.latest_month()

# Calculating the graphs
graph1 = analysis.expenses_by_category_latest_month()
graph2 = analysis.expense_vs_budget_by_category_latest_month()
graph3 = analysis.daily_expenses_latest_month()
graph4 = analysis.expenses_vs_budget_monthly()
graph5 = analysis.expenses_by_category_monthly()

# Creating a class for our graphs
class Graphs:
    def graph1_window(self):

        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 1")
        window.geometry("1000x850")

        # Creating a Top Frame for the Graph 1 window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the Graph 1 window
        frame = LabelFrame(window, text="Graph 1", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure for Graph 1
        fig, ax = plt.subplots(figsize=(8, 6)) 
        ax.pie(graph1['amount'], labels=graph1['category'], autopct='%1.1f%%')
        ax.set_title(f"Expense Distribution during {latest_month}")

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def graph2_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 2")
        window.geometry("1000x850")

        # Creating a Top Frame for the Graph 2 window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the Graph 2 window
        frame = LabelFrame(window, text="Graph 2", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure for Graph 2
        fig, ax = plt.subplots(figsize=(10, 6))
        graph2.plot(kind='bar', ax=ax)
        ax.set_title(f'Expense vs Budget in Each Category during {latest_month}')
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount ($)')
        ax.set_xticklabels(graph2.index, rotation=0) 
        ax.legend(loc='upper left')

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    
    def graph3_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 3")
        window.geometry("1100x850")

        # Creating a Top Frame for the Graph 3 window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the Graph 3 window
        frame = LabelFrame(window, text="Graph 3", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure for Graph 3
        fig, ax = plt.subplots(figsize=(15, 6))  
        for category in graph3.columns:
            ax.plot(
                graph3.index.astype(str), 
                graph3[category], 
                label=f'{category}', 
                marker='o'
            )
        ax.set_xlabel('Days')
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'Daily Expenses during {latest_month}')
        ax.legend(loc='upper left') 

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


    def graph4_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 4")
        window.geometry("1000x850")

        # Creating a Top Frame for the Graph 4 window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the Graph 4 window
        frame = LabelFrame(window, text="Graph 4", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure for Graph 4
        fig, ax = plt.subplots(figsize=(10, 6))  
        graph4.plot(kind='bar', ax=ax)
        ax.set_title('Expenses vs Budget for Each Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_xticklabels(graph4.index, rotation=0)  

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def graph5_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 5")
        window.geometry("1000x850")

        # Creating a Top Frame for the Graph 5 window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the Graph 5 window
        frame = LabelFrame(window, text="Graph 5", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure for Graph 5
        fig, ax = plt.subplots(figsize=(10, 6)) 
        graph5.plot(kind='bar', ax=ax)
        ax.set_title('Amount Spent in Each Category per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_xticklabels(graph5.index, rotation=0)  # Keep x-ticks horizontal
        ax.legend(title='Category', loc='upper left')

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

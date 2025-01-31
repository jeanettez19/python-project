# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime
from data_dynamic import ExpenseAnalysis
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Example usage:
file_path = './datagen_new.xlsx'
analysis = ExpenseAnalysis(file_path)

# Calculate and print budget vs actual values
analysis.calculate_budgeted_vs_actual()

# Process the expense data and calculate monthly, daily, and daily cumulative expenses
analysis.process_expense_data()
analysis.calculate_monthly_expenses()
analysis.calculate_daily_expenses()
analysis.calculate_daily_cumulative_sum()
analysis.calculate_total_budget_and_actual()
analysis.calculate_daily_cumulative_sum_all_categories()  # New method to calculate total cumulative sum for all categories
analysis.calculate_daily_total_spending()  # New method to calculate total daily spending
analysis1 = analysis
analysis2 = analysis
analysis3 = analysis
analysis4 = analysis
analysis5 = analysis


class Graphs:
    def graph1_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 1")
        window.geometry("600x400")


        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Graph 1: Current Month Expenses", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        ax.plot(analysis.daily_cumulative_sum, color='blue', label='Total Spending')
        ax.set_title('Daily Cumulative Spending for All Categories')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount ($)')
        ax.legend()

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def graph2_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 2")
        window.geometry("600x400")

        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Graph 2: Budget vs Expenses", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        analysis2.calculate_total_budget_and_actual()
        ax.pie(
            [analysis2.total_budget, analysis2.total_actual],
            labels=['Budgeted', 'Actual'],
            autopct='%1.1f%%',
            colors=['lightblue', 'salmon'],
            startangle=90,
            explode=(0.1, 0)
        )

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    
    def graph3_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 3")
        window.geometry("600x400")

        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Graph 3: Daily Expenses Over Current Month", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        if not analysis3.daily_total_spending.empty:
            ax.plot(
                analysis3.daily_total_spending.index,
                analysis3.daily_total_spending,
                label='Total Daily Spending',
                linestyle='-',
                color='purple',
                linewidth=2
            )
        ax.set_xlabel('Time')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Total Daily Spending')
        ax.legend()

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)


    def graph4_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 4")
        window.geometry("700x600")

        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Graph 4", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Creating a label for the main window
        Label1 = Label(frame, text="Graph 4: Budget vs Expenses Over Months", font=("Arial", 12)).pack(pady=10)

        # Create the matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        fig, ax = plt.subplots()
        bar_width = 0.35
        x_positions = np.arange(len(analysis4.categories))

        ax.bar(
            x_positions - bar_width / 2,
            analysis4.budgeted,
            bar_width,
            label='Budgeted',
            color='skyblue'
        )
        ax.bar(
            x_positions + bar_width / 2,
            analysis4.actual,
            bar_width,
            label='Actual',
            color='salmon'
        )

        # Set labels, title, and ticks
        ax.set_xlabel('Categories')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Budget vs Actual Expenses')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(analysis4.categories)
        ax.legend()
        ax.tick_params(axis='x')

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def graph5_window(self):
        # Creating a new window
        window = Toplevel(self)
        window.title("Graph 5")
        window.geometry("600x400")

        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to My Finances", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Graph 5: Category Expenses Over Months", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Create the matplotlib figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        fig, ax = plt.subplots()

        # Expense Breakdown (Donut Chart)
        expense_breakdown = analysis5.actual
        wedges, texts, autotexts = ax.pie(
            expense_breakdown,
            labels=analysis5.categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.tab20.colors[:len(analysis5.categories)]
        )

        # Add a center hole to make it a donut chart
        ax.pie([1], radius=0.7, colors=['white'])

        # Rotate the percentage labels
        for autotext in autotexts:
            autotext.set_rotation(0)

        # Set aspect ratio to be equal so that pie is drawn as a circle.
        ax.axis('equal')

        # Embed the figure in the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
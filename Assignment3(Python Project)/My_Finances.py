# Importing the tkinter module for our GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Treeview
from datetime import datetime
from functools import partial
from Graphs import Graphs


class MyFinances:
    def open_MFwindow(self):

        # Creating a new window
        window = Toplevel(self)
        window.title("Expense Tracker")
        window.geometry("700x400")

        # Creating a top_f for the main window
        top_f = Frame(window)
        top_f.pack(padx=5, pady=5, fill="both")
        
        back_button = Button(top_f, text="Return to Main Window", command=window.destroy, bg="Firebrick", fg="White")
        back_button.pack(side=LEFT)

        # Creating a frame for the main window
        frame = LabelFrame(window, text="Analyse Your Finances", padx=30, pady=30, font=("Arial", 12))
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Creating buttons for the main window
        self.button1 = Button(frame, text="Graph 1: Current Month Expenses", command=lambda: Graphs.graph1_window(self), font=("Arial", 12), fg="black")
        self.button1.grid(row=0,column=0,pady=10)

        self.button2 = Button(frame, text="Graph 2: Budget vs Expenses", command=lambda: Graphs.graph2_window(window), font=("Arial", 12), fg="black")
        self.button2.grid(row=0,column=2,pady=10)

        self.button3 = Button(frame, text="Graph 3: Daily Expenses Over Current Month", command=lambda: Graphs.graph3_window(window), font=("Arial", 12), fg="black")
        self.button3.grid(row=1,column=0,pady=10)

        self.button4 = Button(frame, text="Graph 4: Budget vs Expenses Over Months", command=lambda: Graphs.graph4_window(window), font=("Arial", 12), fg="black")
        self.button4.grid(row=1,column=2,pady=10)

        self.button5 = Button(frame, text="Graph 5: Category Expenses Over Months", command=lambda: Graphs.graph5_window(window), font=("Arial", 12), fg="black")
        self.button5.grid(row=2,column=0,columnspan=2,pady=10,padx=10)

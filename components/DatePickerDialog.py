import tkinter as tk
import calendar
from datetime import datetime


class DatePickerDialog:
    """A dialog that displays a calendar popup and returns the selected date."""

    def __init__(self, parent=None, title="Select a Date", firstweekday=6, startdate=None, filter_func=lambda date: True):
        self.filter_func = filter_func

        self.parent = parent
        self.root = tk.Toplevel()
        self.root.attributes("-topmost", True)
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.transient(self.parent)

        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today().date()

        self.date_selected = self.startdate
        self.date = self.startdate
        self.calendar = calendar.Calendar(firstweekday=firstweekday)

        self.titlevar = tk.StringVar()
        self.datevar = tk.IntVar()

        self.root.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self._setup_calendar()
        self.root.grab_set()
        self.root.wait_window()

    def _setup_calendar(self):
        self.frm_calendar = tk.Frame(self.root, bg="white")
        self.frm_calendar.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.frm_title = tk.Frame(self.frm_calendar, bg="white")
        self.frm_title.pack(fill=tk.X)
        self.frm_header = tk.Frame(self.frm_calendar, bg="white")
        self.frm_header.pack(fill=tk.X)

        self._draw_titlebar()
        self._draw_calendar()

    def _draw_calendar(self):
        self._set_title()
        self._current_month_days()
        
        self.frm_dates = tk.Frame(self.frm_calendar, bg="white")
        self.frm_dates.pack(fill=tk.BOTH, expand=tk.YES)

        for row, weekday_list in enumerate(self.monthdays):
            for col, day in enumerate(weekday_list):
                self.frm_dates.columnconfigure(col, weight=1)
                if day == 0:
                    tk.Label(self.frm_dates, text="", bg="white", width=4).grid(row=row, column=col, sticky=tk.NSEW)
                else:
                    selectable = self.filter_func(self.monthdates[row][col])
                    fg_color = "black" if selectable else "gray"
                    state = tk.NORMAL if selectable else tk.DISABLED
                    tk.Button(
                        self.frm_dates,
                        text=str(day),
                        fg=fg_color,
                        state=state,
                        command=lambda x=row, y=col: self._on_date_selected(x, y),
                    ).grid(row=row, column=col, sticky=tk.NSEW, padx=2, pady=2)

    def _draw_titlebar(self):
        self.prev_period = tk.Button(
            self.frm_title, text="\xab", command=self.on_prev_month, width=3
        )
        self.prev_period.pack(side=tk.LEFT)

        self.title = tk.Label(self.frm_title, textvariable=self.titlevar, bg="white", font=("Arial", 12))
        self.title.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.next_period = tk.Button(
            self.frm_title, text="\xbb", command=self.on_next_month, width=3
        )
        self.next_period.pack(side=tk.LEFT)

        for col in self._header_columns():
            tk.Label(self.frm_header, text=col, bg="white", font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

    def _set_title(self):
        _titledate = f'{self.date.strftime("%B %Y")} '
        self.titlevar.set(_titledate.capitalize())

    def _current_month_days(self):
        self.monthdays = self.calendar.monthdayscalendar(
            year=self.date.year, month=self.date.month
        )
        self.monthdates = self.calendar.monthdatescalendar(
            year=self.date.year, month=self.date.month
        )

    def _header_columns(self):
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        return weekdays[self.firstweekday:] + weekdays[:self.firstweekday]

    def _on_date_selected(self, row, col):
        self.date_selected = self.monthdates[row][col]
        self.root.destroy()

    def _on_cancel(self):
        self.date_selected = None
        self.root.destroy()

    def on_next_month(self):
        year, month = self._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def on_prev_month(self):
        year, month = self._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self._refresh_calendar()

    def _refresh_calendar(self):
        self.frm_dates.destroy()
        self._draw_calendar()

    @staticmethod
    def _nextmonth(year, month):
        return (year + 1, 1) if month == 12 else (year, month + 1)

    @staticmethod
    def _prevmonth(year, month):
        return (year - 1, 12) if month == 1 else (year, month - 1)


if __name__ == "__main__":
    def select_date():
        chooser = DatePickerDialog(parent=button, title="Choose a date", filter_func=lambda x: True)
        label.config(text=chooser.date_selected)

    root = tk.Tk()
    root.geometry("400x300")

    label = tk.Label(root, text="Choose date")
    label.pack(padx=10, pady=10)

    button = tk.Button(root, text="Select date", command=select_date)
    button.pack(padx=10, pady=10)

    root.mainloop()

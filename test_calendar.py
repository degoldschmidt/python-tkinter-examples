import tkinter as tk
import ttkcalendar

import tkSimpleDialog


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection

# Demo code:


class CalendarFrame(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text="CalendarDialog Demo")

        def getdate():
            cd = CalendarDialog(self)
            result = cd.result
            self.selected_date.set(result.strftime("%m/%d/%Y"))

        self.selected_date = tk.StringVar()

        tk.Entry(self, textvariable=self.selected_date).pack(side=tk.LEFT)
        tk.Button(self, text="Choose a date", command=getdate).pack(side=tk.LEFT)


def main():
    root = tk.Tk()
    root.wm_title("CalendarDialog Demo")
    CalendarFrame(root).pack()
    root.mainloop()

if __name__ == "__main__":
    main()

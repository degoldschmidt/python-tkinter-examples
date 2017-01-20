#!/usr/bin/env python
# coding: UTF-8

try:
    #~~ For Python 2.x
    import Tkinter as tk
except ImportError:
    #~~ For Python 3.x
    import tkinter as tk

APP_WIN_XPOS = 100
APP_WIN_YPOS = 100
APP_WIN_WIDTH = 500
APP_WIN_HEIGHT = 500
APP_WIN_TITLE = 'Overlapping Widgets'
APP_BACK_GND = 'palegoldenrod'

MSG_01 = 'Lower Frame'
MSG_02 = 'Lift Frame'

class App(object):

    def __init__(self):

        self.win = tk.Tk()
        self.win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
        self.win.geometry('{0}x{1}'.format(APP_WIN_WIDTH, APP_WIN_HEIGHT))
        self.win.protocol("WM_DELETE_WINDOW", self.close)
        self.win.config(bg=APP_BACK_GND)

        self.swap_state = tk.StringVar()

        canvas = tk.Canvas(self.win, highlightthickness=0,
            bg='steelblue')
        canvas.place(x=20, y=20, width=300, height=300)

        self.frame = tk.Frame(self.win, bg='green')
        self.frame.place(x=200, y=200, width=200, height=200)

        tk.Button(self.win, textvariable=self.swap_state,
            command=self.swap).pack(side='bottom', pady=2)

        self.swap_state.set(MSG_01)

    def swap(self):
        message = self.swap_state.get()
        if message == MSG_01:
            self.frame.lower()
            self.swap_state.set(MSG_02)

        if message == MSG_02:
            self.frame.lift()
            self.swap_state.set(MSG_01)

    def close(self):
        self.win.destroy()
        print ("Shut down application")

    def run(self):
        self.win.mainloop()

app = App()
app.win.title("Tk App Templates")

app.run()

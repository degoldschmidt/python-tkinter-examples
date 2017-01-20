from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as font
import time as t
import datetime as dt
from draglistbox import Drag_and_Drop_Listbox
import os
from PIL import ImageTk

bgcols =   ["#22A7F0", "#21A6E5", "#20A5DB", "#1FA4D1", "#1FA4C7", "#1EA3BD", "#1DA2B2", "#1CA1A8", "#1CA19E", "#1BA094", "#1A9F8A", "#1A9F80"]

def bodyfont(size):
    return font.Font(family='Dosis Light', size=size, weight='normal')

def titlefont(size):
    return font.Font(family='Dosis', size=size, weight='normal')

def fixedfont(size):
    return font.Font(family='Source Code Pro Light', size=size, weight='normal')

class Timer():
    def __init__(self):
        self.timestart = dt.datetime.now()
        self.started = False
        self.elapsed = dt.datetime.now() - self.timestart

    def get(self):
        mins, secs = divmod(self.elapsed.total_seconds(), 60)
        return '{0:02d}'.format(int(mins))+":"+'{0:02d}'.format(int(secs))

    def reset(self):
        self.timestart = dt.datetime.now()

    def start(self):
        self.started = True

    def stop(self):
        if not self.started:
            self.reset()
        self.started = False

    def update(self):
        if self.started:
            self.elapsed = dt.datetime.now() - self.timestart
        else:
            self.timestart = dt.datetime.now()
            self.elapsed = dt.datetime.now() - self.timestart


class App():
    def __init__(self):

        ### ROOT WINDOW
        self.root = Tk()
        self.root.title("FlyPAD Experiments UI")
        # make it cover the entire screen
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.focus_set()
        #self.root.call("::tk::unsupported::MacWindowStyle", "style", self.root, "plain", "none")
        self.root.attributes("-fullscreen",True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_state("zoomed")
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        ### STYLE
        # colors
        self.clock = Label(self.root, text="")
        self.clock.place(relx=0.9, rely=0.1, anchor = CENTER)
        self.timings = [Timer(), Timer(), Timer(), Timer(), Timer()]
        self.main = LabelFrame(self.root, height=2, bd=1, relief=FLAT, padx=0.5)
        self.main.place(relx=0.5, rely=0.6, anchor = CENTER)
        self.timer = [Label(self.main, text="00:00"), Label(self.main, text="00:00"), Label(self.main, text="00:00"), Label(self.main, text="00:00"), Label(self.main, text="00:00")]
        self.status = [Label(self.main, text="STOPPED"), Label(self.main, text="STOPPED"), Label(self.main, text="STOPPED"), Label(self.main, text="STOPPED"), Label(self.main, text="STOPPED")]
        self.setTime()

        # title
        self.title = Label(self.root, text="FlyPAD Experiments UI")
        self.title.place(relx=0.5, rely=0.1, anchor = CENTER)

        # main grid
        epad = 30
        expad = 60
        bxpad = 10
        lxpad = 60
        Label(self.main, text="Filename", font=titlefont(24), bg=self.current_bg, fg="white").grid(row=0,column=1, pady=epad)
        Label(self.main, text="Start/stop", font=titlefont(24), bg=self.current_bg, fg="white").grid(row=0,column=2, columnspan=2, pady=epad)
        Label(self.main, text="Timer", font=titlefont(24), bg=self.current_bg, fg="white").grid(row=0,column=4, pady=epad)
        Label(self.main, text="Status", font=titlefont(24), bg=self.current_bg, fg="white").grid(row=0,column=5, pady=epad)
        for i in range(5):
            Label(self.main, text="FlyPAD "+str(i+1), font=bodyfont(24), bg=self.current_bg).grid(row=i+1,column=0, pady=epad)
            Entry(self.main, width=30).grid(row=i+1,column=1, pady=epad, padx= expad)
            Button(self.main, text="▶", font=titlefont(12), fg=self.current_bg, command=self.timings[i].start).grid(row=i+1,column=2, pady=epad, padx= bxpad)
            Button(self.main, text="■", font=titlefont(24), fg=self.current_bg, command=self.timings[i].stop).grid(row=i+1,column=3, pady=epad, padx= bxpad)
            self.timer[i].config(fg="white", bg=self.current_bg, font=fixedfont(24))
            self.timer[i].grid(row=i+1,column=4, pady=epad, padx= lxpad)
            self.status[i].config(fg="white", bg=self.current_bg, font=bodyfont(24))
            self.status[i].grid(row=i+1,column=5, pady=epad, padx= bxpad)
        self.title.configure(font=titlefont(84), fg="white", bg=self.current_bg)
        self.main.configure(bg=self.current_bg, borderwidth=10, font=bodyfont(18), fg="white")
        #self.loc1.configure(bg=self.current_bg)
        self.clock.config(fg="white", bg=self.current_bg, font=bodyfont(30))

        # ttk styles
        self.style = ttk.Style()

        self.update()

    def destroy(self):
        self.root.destroy()

    def setTime(self):
        hour = int(t.strftime("%H", t.localtime()))
        if (hour-9) < 0 or (hour-9)>(len(bgcols)-1):
            self.current_bg = "#22313F"  ### nighttime color
        else:
            self.current_bg = bgcols[hour-9]
        ## set current time
        now = t.strftime("%a, %d %b %Y\n%H:%M:%S" , t.localtime())
        for i in range(5):
            self.timings[i].update()
            if self.timings[i].started:
                status_color = "red"
                status_text = "RUNNING"
            else:
                status_color = "white"
                status_text = "STOPPED"
            self.status[i].configure(text=status_text, fg=status_color)
            self.timer[i].configure(text=self.timings[i].get(), bg=self.current_bg)
        self.clock.configure(text=now, bg=self.current_bg)
        self.root.configure(background=self.current_bg)

    def update(self):
        self.setTime()
        self.root.after(100, self.update)

def main():
    app = App()
    app.root.mainloop()

if __name__ == '__main__':
    main()

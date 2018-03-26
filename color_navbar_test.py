import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W, messagebox
from PIL import Image, ImageTk
import threading
import webbrowser
import json
import os

# My modules
#import twitch_data as twitch
#import color
#import font
#import style

def dit(*args):
    pass

light_grey = '#616161'
dark_purple = '#8700e6'
light_purple = '#bf77ff'
blue = '#0044ff'

class TestApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        init_styles()
        #self.parent = parent
        #self.init_frames()
        #self.grid_frames()
        ttk.Label(parent, text = 'Experiments', style='TLabel').grid(row=0, column=0)

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.s = None
        init_styles()
        self.parent = parent
        self.init_frames()
        self.grid_frames()

    def init_frames(self):
        self.navbar = Navbar(self)
        experiments = Experiments(self)
        videos = Videos(self)
        sessions = Sessions(self)
        datasets = Datasets(self)
        self.sections = [experiments, videos, sessions, datasets]

    def grid_frames(self):
        self.navbar.grid(row = 0, column = 0)
        for section in self.sections:
            section.grid(row = 0, column = 1, sticky = (N))
            section.grid_remove()
        self.section_changed(self.navbar.selection)

    def section_changed(self, index):
        for section in self.sections:
            section.grid_remove()
        self.sections[index].grid()

class Navbar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        base_icon='icon'
        self.sections = [[ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'experiments_tiny.png'))), 'Experiments'], [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'videos.png'))), 'Videos'], [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'sessions.png'))), 'Sessions'], [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'datasets.png'))), 'Datasets']]
        self.frames = []
        self.selection = 0
        self.init_widgets()
        self.change_style(self.frames[self.selection], 'light.TFrame', 'light.TLabel')
        self.grid_widgets()

    def init_widgets(self):
        # Frameception
        for index, section in enumerate(self.sections):
            frame = ttk.Frame(self, style = 'dark.TFrame')
            li = ttk.Label(frame, image = section[0], style = 'dark.TLabel')
            lt = ttk.Label(frame, text = section[1], style = 'dark.TLabel')
            frame.bind('<Enter>', self.enter)
            frame.bind('<Leave>', self.leave)
            #li.bind('<Button-1>', self.click)
            #lt.bind('<Button-1>', self.click)
            frame.bind('<Button-1>', self.click)
            self.frames.append(frame)
        self.label_filler = tk.Label(self, text = '', bg = dark_purple, height = 100)

    def grid_widgets(self):
        for index_frame, frame in enumerate(self.frames):
            for index_child, child in enumerate(frame.winfo_children()):
                child.grid(row = 0, column = index_child, padx = (0, 25 * index_child))
            frame.grid(row = index_frame, column = 0, sticky = (E, W))
        self.label_filler.grid(row = len(self.sections), column = 0, sticky = (E, W))

    def enter(self, event):
        self.change_style(event.widget, 'dark.TFrame', 'light.TFrame')

    def leave(self, event):
        if self.frames.index(event.widget) != self.selection:
            self.change_style(event.widget, 'light.TFrame', 'dark.TFrame')

    def click(self, event):
        if event.widget.winfo_class() == 'TFrame':
            index = self.frames.index(event.widget)
        else:
            index = self.frames.index(event.widget.master)
        if index != self.selection:
            self.change_style(self.frames[self.selection], 'dark.TFrame', 'light.TLabel')
            self.selection = index
            self.parent.section_changed(index)

    def change_style(self, widget, style_w, style_c):
        """Change the style of a widget and its children."""
        widget.configure(style = style_w)
        for child in widget.winfo_children():
            child.configure(style = style_c)

class Experiments(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.label = ttk.Label(self, text = 'Experiments')

    def grid_widgets(self):
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10)

class Videos(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.label = ttk.Label(self, text = 'Videos')

    def grid_widgets(self):
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10)

class Sessions(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.label = ttk.Label(self, text = 'Sessions')

    def grid_widgets(self):
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10)

class Datasets(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.s = None #self.import_settings()
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        pass

    def grid_widgets(self):
        pass


def defocus(event):
    event.widget.master.focus_set()

def init_styles():
    print('init styles')
    s = ttk.Style()
    s.configure('TFrame', background = light_grey)
    s.configure('TLabel', font = ('Open Sans', 12, 'roman'), background = light_grey)
    s.configure('TButton', padding = 2, font = ('Open Sans', 10, 'regular'))
    s.configure('TEntry')
    s.configure('TLabelframe', background = light_grey)
    s.configure('TCheckbutton', background = light_grey, font = ('Open Sans', 10, 'regular'))

    s.configure('large.TLabel', background = light_grey, font = ('Open Sans', 14, 'regular'))
    s.configure('medium.TLabel', background = light_grey, font = ('Open Sans', 12, 'regular'))
    s.configure('small.TLabel', background = light_grey, font = ('Open Sans', 10, 'regular'))
    s.configure('tiny.TLabel', background = light_grey, font = ('Open Sans', 8, 'regular'))

    s.configure('hyper.TLabel', background = light_grey, foreground = blue, cursor = 'hand2', font = ('Open Sans', 10, 'regular'))

    s.configure('dark.TFrame', background = dark_purple)
    s.configure('light.TFrame', background = light_purple)
    s.configure('dark.TLabel', background = dark_purple, font = ('Open Sans', 12, 'regular'))
    s.configure('light.TLabel', background = light_purple, font = ('Open Sans', 12, 'regular'))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Colored Navbar Test')
    #root.iconbitmap(default = 'icon.ico')
    root.geometry('1000x500')
    root.configure(bg = light_grey)
    #MainApplication(root).grid(row = 0, column = 0, sticky = (N, E, S, W))
    TestApp(root).grid(row = 0, column = 0, sticky = (N, E, S, W))
    root.mainloop()

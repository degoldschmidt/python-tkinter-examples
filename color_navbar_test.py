import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W, messagebox
from PIL import Image, ImageTk
import threading
import webbrowser
import json
import os
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt

from tkinter_png import *

def dit(*args):
    pass

light_grey = '#616161'
dark_purple = '#8700e6'
light_purple = '#bf77ff'
blue = '#0044ff'

def get_images(paths):

    return [PhotoImage(file=path) for path in paths]##[ImageTk.PhotoImage(img) for img in pil_img]

class TestApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        init_styles()
        self.parent = parent
        self.init_frames()
        self.grid_frames()

    def init_frames(self):
        self.navbar = ColorNavBar(self)
        experiments = EmptyFrame(self)
        videos = EmptyFrame(self)
        sessions = EmptyFrame(self)
        datasets = EmptyFrame(self)
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

class ColorNavBar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selection = 0

        base_icon='icon'
        section_names = ['Experiments', 'Videos', 'Sessions', 'Datasets'] #icon.jpeg'
        image_files = [os.path.join(base_icon, name.lower()+'.png') for name in section_names]
        images = get_images(image_files)
        self.sections = [(image, section) for image, section in zip(images, section_names)]
        self.frames = []
        self.list_img = section_names
        self.selection = 0
        self.init_widgets()
        #self.change_style(self.frames[self.selection], 'light.TFrame', 'light.TLabel')
        self.grid_widgets()

    def init_widgets(self):
        # Frameception
        for index, section in enumerate(self.sections):
            frame = ttk.Frame(self, style = 'dark.TFrame')
            print(section)
            self.list_img[index] = ttk.Label(frame, image = section[0], style = 'dark.TLabel')
            self.list_img[index].image = section[0] # keep a reference!
            lt = ttk.Label(frame, text = section[1], style = 'dark.TLabel')
            #frame.bind('<Enter>', self.enter)
            #frame.bind('<Leave>', self.leave)
            self.list_img[index].bind('<Button-1>', self.click)
            lt.bind('<Button-1>', self.click)
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

class EmptyFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.label = ttk.Label(self, text = 'Empty')

    def grid_widgets(self):
        self.label.grid(row = 0, column = 0, padx = 10, pady = 10)

def defocus(event):
    event.widget.master.focus_set()

def init_styles():
    print('init styles')
    s = ttk.Style()
    s.theme_use('clam')
    print(s.theme_names(), s.theme_use())

    s.configure('TFrame', background = light_grey)
    s.configure('TLabel', font = ('Quicksand', 12, 'roman'), background = light_grey)
    s.configure('TButton', padding = 2, font = ('Quicksand', 10, 'roman'))
    s.configure('TEntry')
    s.configure('TLabelframe', background = light_grey)
    s.configure('TCheckbutton', background = light_grey, font = ('Quicksand', 10, 'roman'))

    s.configure('large.TLabel', background = light_grey, font = ('Quicksand', 14, 'roman'))
    s.configure('medium.TLabel', background = light_grey, font = ('Quicksand', 12, 'roman'))
    s.configure('small.TLabel', background = light_grey, font = ('Quicksand', 10, 'roman'))
    s.configure('tiny.TLabel', background = light_grey, font = ('Quicksand', 8, 'roman'))

    s.configure('hyper.TLabel', background = light_grey, foreground = blue, cursor = 'hand2', font = ('Quicksand', 10, 'roman'))

    s.configure('dark.TFrame', background = dark_purple)
    s.configure('light.TFrame', background = light_purple)
    s.configure('dark.TLabel', background = dark_purple, font = ('Quicksand', 12, 'roman'))
    s.configure('light.TLabel', background = light_purple, font = ('Quicksand', 12, 'roman'))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Colored Navbar Test')
    #root.iconbitmap(default = 'icon.ico')
    root.geometry('1000x500')
    root.configure(bg = light_grey)
    #MainApplication(root).grid(row = 0, column = 0, sticky = (N, E, S, W))
    TestApp(root).grid(row = 0, column = 0, sticky = (N, E, S, W))
    root.mainloop()

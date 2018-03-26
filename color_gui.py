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
        #videos = Videos(self)
        #sessions = Sessions(self)
        #datasets = Datasets(self)
        self.sections = [experiments] #, videos, sessions, datasets]
        #thread_ttv = threading.Thread(target = dit, args = (None, 50))
        #thread_ttv.start()

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
        #base_icon = os.path.join('.','icon')
        base_icon='icon'
        self.sections = [[ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'experiments_tiny.png'))), 'Experiments']]
        #, [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'videos.png'))), 'Videos'], [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'sessions.png'))), 'Sessions'], [ImageTk.PhotoImage(Image.open(os.path.join(base_icon, 'datasets.png'))), 'Datasets']]
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
            li.bind('<Button-1>', self.click)
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
        self.change_style(event.widget, 'light.TFrame', 'light.TLabel')

    def leave(self, event):
        if self.frames.index(event.widget) != self.selection:
            self.change_style(event.widget, 'dark.TFrame', 'dark.TLabel')

    def click(self, event):
        if event.widget.winfo_class() == 'TFrame':
            index = self.frames.index(event.widget)
        else:
            index = self.frames.index(event.widget.master)
        if index != self.selection:
            self.change_style(self.frames[self.selection], 'dark.TFrame', 'dark.TLabel')
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

"""
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
        self.label_quality = ttk.Label(self, text = 'Stream quality', style = 'medium.TLabel')
        self.quality = Quality(self, labelwidget = self.label_quality)

        self.label_chat = ttk.Label(self, text = 'Chat', style = 'medium.TLabel')
        self.chat = Chat(self, labelwidget = self.label_chat)

        self.label_tokenf = ttk.Label(self, text = 'Token', style = 'medium.TLabel')
        self.tokenf = Tokenf(self, labelwidget = self.label_tokenf)

    def grid_widgets(self):
        self.quality.grid(row = 0, column = 0, sticky = (E, W), padx = 20, pady = 10)
        self.chat.grid(row = 1, column = 0, sticky = (E, W), padx = 20, pady = 10)
        self.tokenf.grid(row = 2, column = 0, sticky = (E, W), padx = 20, pady = 10)

    def import_settings(self):
        with open('settings.json', 'r') as f:
            return json.load(f)

    def export_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.parent.s, f, sort_keys = True, indent = 4)

    def setting_changed(self, setting, value):
        self.parent.s[setting.lower()] = value
        self.export_settings()

class Quality(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.stream_quality = tk.StringVar()
        self.qualities = ['Source (best)', 'High', 'Medium', 'Low', 'Mobile (worst)', 'Audio only']
        self.qualities_lower = ['source', 'high', 'medium', 'low', 'mobile', 'audio']
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.cb_quality = ttk.Combobox(self, state = 'readonly', textvariable = self.stream_quality, values = self.qualities)
        #self.cb_quality.current(self.qualities_lower.index(self.parent.parent.s['quality']))
        self.cb_quality.bind('<<ComboboxSelected>>', self.cb_changed)
        self.cb_quality.bind('<FocusIn>', defocus)

    def grid_widgets(self):
        self.cb_quality.grid(row = 0, column = 0, padx = 10, pady = 10)

    def cb_changed(self, event):
        q = self.stream_quality.get().split()[0].lower()
        self.parent.setting_changed('quality', q)

class Chat(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.open_chat = tk.IntVar()
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.cbutton_chat = ttk.Checkbutton(self, text = 'Open chat', variable = self.open_chat, command = self.cbutton_changed)
        #self.open_chat.set(self.parent.parent.s['chat'])
        self.cbutton_chat.bind('<FocusIn>', defocus)

    def grid_widgets(self):
        self.cbutton_chat.grid(row = 0, column = 0, padx = 10, pady = 10)

    def cbutton_changed(self):
        self.parent.setting_changed('chat', self.open_chat.get())

class Tokenf(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_widgets()
        self.grid_widgets()

    def init_widgets(self):
        self.button_change = ttk.Button(self, text = 'Change', command = lambda: Login(self))

    def grid_widgets(self):
        self.button_change.grid(row = 0, column = 0, padx = 10, pady = 10)

class Login(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.token_var = tk.StringVar()
        self.url = 'http://twitchapps.com/tmi/'
        self.configure_frame()
        self.init_widgets()
        self.grid_widgets()

    def configure_frame(self):
        self.configure(padx = 10, pady = 10, bg = light_grey)
        self.title('Change token')

    def init_widgets(self):
        self.label_token = ttk.Label(self, text = 'Token: ')
        self.label_tokenlink = ttk.Label(self, text = 'Generate', cursor = 'hand2', style = 'hyper.TLabel')
        self.label_tokenlink.bind('<Button-1>', self.get_token)
        self.entry_token = ttk.Entry(self, textvariable = self.token_var, width = 40, font = ('Open Sans', 10, 'regular'))
        self.entry_token.bind('<Return>', self.login)
        self.button_login = ttk.Button(self, text = 'OK', command = self.login)

    def grid_widgets(self):
        self.label_token.grid(row = 0, column = 0, sticky = (W))
        self.label_tokenlink.grid(row = 1, column = 0, sticky = (W), pady = (10, 0))
        self.entry_token.grid(row = 0, column = 1)
        self.button_login.grid(row = 1, column = 1, sticky = (E), pady = (10, 0))

    def get_token(self, event):
        webbrowser.open_new(self.url)

    def login(self, *args):
        token = True #twitch.fix_token(self.token_var.get())
        if token:
            #self.parent.parent.setting_changed('token', token)
            self.destroy()
        else:
            messagebox.showinfo(parent = self, title = 'Error', message = 'Invalid token format', icon = 'error')
"""

def defocus(event):
    event.widget.master.focus_set()

def init_styles():
    print('init styles')
    s = ttk.Style()
    s.configure('regular.TFrame', background = light_grey)
    s.configure('regular.TLabel', background = light_grey, font = ('Open Sans', 10, 'regular'))
    s.configure('regular.TButton', padding = 2, font = ('Open Sans', 10, 'regular'))
    s.configure('regular.TEntry')
    s.configure('regular.TLabelframe', background = light_grey)
    s.configure('regular.TCheckbutton', background = light_grey, font = ('Open Sans', 10, 'regular'))

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
    root.title('TTV')
    #root.iconbitmap(default = 'icon.ico')
    root.geometry('1000x500')
    root.configure(bg = light_grey)
    MainApplication(root).grid(row = 0, column = 0, sticky = (N, E, S, W))
    root.mainloop()

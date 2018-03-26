import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox, filedialog
import sys, os
import io, yaml

class DataBase(object):
    def __init__(self):
        self.data = {'experiments': [],
                         'videos': [],
                         'session': [],
                         'dataset': []}

    def add_experiment(self, name, date, status, **kwargs):
        self.data['experiments'].append(name)
        entry = {}
        entry['id'] = "{:05d}".format(len(self.data['experiments']) - 1)
        entry['name'] = name
        entry['date'] = date
        entry['status'] = status
        ### extra entries
        for kw,v in kwargs.items():
            entry[kw] = v

        with open('./data/experiments/{}_{}.yaml'.format(entry['id'], entry['name']), 'w', encoding='utf8') as f:
            yaml.dump(entry, f, default_flow_style=False, allow_unicode=True, canonical=False)

    def filter(self, val):
        self.view = self.data.copy()
        for k, v in self.data.items():
            if val in k or val in v:
                pass
            else:
                self.view = self.view.pop(k)

class MultiList(object):
    """
    A Tkinter listbox with drag'n'drop reordering of entries and columns.
    """
    def __init__(self, master, cols, **kw):
        self.master = master
        container = ttk.Frame(master)
        container.pack(fill='both', expand=True)
        self.tree = ttk.Treeview(columns=cols, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, columnspan=4, row=0, sticky='nsew', in_=container)
        vsb.grid(column=4, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, columnspan=4, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.oldf = ""
        self.filter = tk.StringVar()
        self.entry = tk.Entry(container, textvariable=self.filter)
        self.entry.grid(column=0, row=2, sticky='nsew', in_=container)
        self.button = tk.Button(container, text='Add')
        self.button.grid(column=1, row=2, sticky='nsew', in_=container)
        self.button = tk.Button(container, text='Edit')
        self.button.grid(column=2, row=2, sticky='nsew', in_=container)
        self.button = tk.Button(container, text='Remove')
        self.button.grid(column=3, row=2, sticky='nsew', in_=container)
        self.columns = cols
        for col in cols:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        ### Bindings
        self.tree.bind("<ButtonPress-1>", self.select)
        self.tree.bind("<ButtonRelease-1>", self.release, add='+')
        self.tree.bind("<B1-Motion>",self.move, add='+')
        self.tree.bind("<ButtonPress-2>", self.popup)
        self.tree.bind("<Command-Up>", self.key)
        self.tree.bind("<Control-Down>", self.move_down)
        self.popup_menu = tk.Menu(self.tree, tearoff=0)
        self.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
        self.popup_menu.add_command(label="Select All",
                                    command=self.select_all)

        ### update loop
        self._update()

    def _update(self):
        if self.oldf != self.filter.get():
            #print(self.filter.get())
            self.oldf = self.filter.get()
        self.master.after(100, self._update)

    def add(self, entry):
        _group = self.tree.insert('', 'end', values=entry)
        for ix, val in enumerate(entry):
            col_w = tkFont.Font().measure(val)
            if self.tree.column(self.columns[ix],width=None)<col_w:
                self.tree.column(self.columns[ix], width=col_w)

    def key(self, event):
        print(event.keycode)


    def move(self, event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))
        for s in tv.selection():
            tv.move(s, '', moveto)

    def move_down(self, event):
        tv = event.widget
        for s in tv.selection():
            tv.move(s, '', s-1)

    def move_up(self, event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))
        print('MoveUp')
        for s in tv.selection():
            print(s)
            tv.move(s, '', s+1)

    def options(self, event):
        selected = tv.index(tv.identify_row(event.y))

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root+50, event.y_root+20, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        for i in self.tree.curselection()[::-1]:
            self.tree.delete(i)

    def release(self, event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def select_all(self):
        self.tree.selection_set(0, 'end')

    def select(self, event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, \
            int(not descending)))

class MenuBar(object):
    def __init__(self, frame, struct):
        self.menu = tk.Menu()
        frame.config(menu=self.menu)
        for cascade, command in struct.items():
            submenu = tk.Menu(self.menu)
            self.menu.add_cascade(label=cascade, menu=submenu)
            for label, func in command.items():
                if '&sep' in label: submenu.add_separator()
                else: submenu.add_command(label=label, command=func)

class NoteBook(ttk.Notebook):
    def __init__(self, frame, struct):
        ttk.Notebook.__init__(self)
        self.tabs = {}
        for k, v in struct.items():
            self.tabs[k] = tk.Frame(self)
            self.add(self.tabs[k], text=k)
        self.pack(fill=tk.BOTH,expand=1)


class MainWindow(object):
    def __init__(self, master):
        self.master = master

        ### if first time user (save in home folder)
        ### TODO: create folder and profile file

        ### database objects
        self.dir = os.getcwd()
        self.db = DataBase()
        self.currfile = None

        ### system adjustments
        if sys.platform == 'darwin':
            s = ttk.Style()
            s.configure('TNotebook', tabposition='nw')
            s.configure('TNotebook.Tab', padding=(20, 8, 20, 0))

        ### general
        self.master.title("pyTrack-GUI v1.0".format(self.currfile))
        self.master.resizable(width=True, height=True)
        self.master.geometry("800x600")

        ### menubar
        self.menubar = MenuBar(self.master, {   'File': {'New': self.new_db, 'Open...': self.load_db, 'Open recent': None, 'Save': self.save_db, 'Save as...': self.saveas_db, '&sep1': None, 'Import': None, 'Export': None, '&sep2': None, 'Quit': self.master.destroy},
                                                'Edit': {'Undo': None, 'Redo': None, '&sep1': None, 'Cut': None, 'Copy': None, 'Paste': None, '&sep2': None, 'Preferences': None},
                                                'View': {'Toggle fullscreen': None},
                                                'Window': {'Minimize': None},
                                                'Help': {'About': None}})

        ### notebook tabs
        self.notebook = NoteBook(self.master, { ##'Stocks': None,
                                                'Experiments': None,
                                                'Videos': None,
                                                'Sessions': None,
                                                'Datasets': None})

        ### setup Experiments tab
        exps_tab = self.notebook.tabs['Experiments']
        self.exp_list = MultiList(exps_tab, ['ID', 'Title', 'Starting date', 'Status'], height=10)

        self.exp_list.add(['0000', 'Example Experiment', '24.11.2018', 'Completed'])
        self.db.add_experiment('Example Experiment', '24.11.2018', 'Completed')
        self.exp_list.add(['0001', 'Example Experiment 2', '26.11.2018', 'In progress'])
        self.db.add_experiment('Example Experiment 2', '26.11.2018', 'In progress')
        self.exp_list.add(['0002', 'Example Experiment 3', '29.11.2018', 'Planned'])
        self.db.add_experiment('Example Experiment 3', '29.11.2018', 'Planned')

        self._update()

    def _update(self):
         pass

    def load_db(self):
        askload = messagebox.askquestion("Load file", "Are you sure to load a database from file? All unsaved data will be lost.", icon='warning')
        if askload == 'yes':
            self.currfile = filedialog.askopenfilename(title='Load database file', initialdir=self.dir)
            with open(self.currfile, 'r') as stream:
                self.db = yaml.load(stream)
            self.master.title("pyTrack-GUI v1.0 - {}".format(self.currfile))

    def new_db(self):
        askload = messagebox.askquestion("New file", "Are you sure to open a new database? All unsaved data will be lost.", icon='warning')
        if askload == 'yes':
            self.currfile = None
            self.db = DataBase()
            self.master.title("pyTrack-GUI v1.0 - {}".format(self.currfile))

    def saveas_db(self):
        self.currfile = filedialog.asksaveasfilename(title='Save database file', initialdir=self.dir)
        self.save_db()

    def save_db(self):
        if self.currfile is None:
            self.saveas_db()
        with io.open(self.currfile, 'w+', encoding='utf8') as f:
            yaml.dump(self.db, f, default_flow_style=False, allow_unicode=True, canonical=False)
        self.master.title("pyTrack-GUI v1.0 - {}".format(self.currfile))


if __name__ == '__main__':
    root = tk.Tk()
    myApp = MainWindow(root)
    root.mainloop()

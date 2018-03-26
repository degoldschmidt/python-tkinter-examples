'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def bind(self, name, func, add=""):
        self.tree.bind(name, func, add)

    def _setup_widgets(self):
        s = """\click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in car_list:
            if type(item) is list:
                print(item[0])
                _group = self.tree.insert('', 'end', item[0], values=item[0])
                for subitem in item[1:]:
                    self.tree.insert(_group, 'end', values=subitem)
            else:
                self.tree.insert('', 'end',text=item[0], values=item[1:])
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)

def sortby(tree, col, descending):
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
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

# the test data ...

car_header = ['car', 'repair','more']
car_list = [
['cars', ('this', "mothafucking", 'car')],
('Hyundai', 'brakes', "this") ,
('Honda', 'light') ,
('Lexus', 'battery') ,
('Benz', 'wiper') ,
('Ford', 'tire') ,
('Chevy', 'air') ,
('Chrysler', 'piston') ,
('Toyota', 'brake pedal') ,
('BMW', 'seat'),
('Hyundai', 'brakes') ,
('Honda', 'light') ,
('Lexus', 'battery') ,
('Benz', 'wiper') ,
('Ford', 'tire') ,
('Chevy', 'air') ,
('Chrysler', 'piston') ,
('Toyota', 'brake pedal') ,
('BMW', 'seat')
]

def bDown_Shift(event):
    tv = event.widget
    select = [tv.index(s) for s in tv.selection()]
    select.append(tv.index(tv.identify_row(event.y)))
    select.sort()
    for i in range(select[0],select[-1]+1,1):
        tv.selection_add(tv.get_children()[i])

def bDown(event):
    tv = event.widget
    if tv.identify_row(event.y) not in tv.selection():
        tv.selection_set(tv.identify_row(event.y))

def bUp(event):
    tv = event.widget
    if tv.identify_row(event.y) in tv.selection():
        tv.selection_set(tv.identify_row(event.y))

def bUp_Shift(event):
    pass

def bMove(event):
    tv = event.widget
    moveto = tv.index(tv.identify_row(event.y))
    for s in tv.selection():
        tv.move(s, '', moveto)


if __name__ == '__main__':
    """
    root = tk.Tk()

    tree = ttk.Treeview(columns=("col1","col2"),
                        displaycolumns="col2",
                        selectmode='none')

    # insert some items into the tree
    for i in range(10):
        tree.insert('', 'end',iid='line%i' % i, text='line:%s' % i, values=('', i))

    tree.grid()
    root.mainloop()
    """
    root = tk.Tk()
    root.title("Multicolumn Treeview/Listbox")
    listbox = MultiColumnListbox()
    listbox.bind("<ButtonPress-1>",bDown)
    listbox.bind("<ButtonRelease-1>",bUp, add='+')
    listbox.bind("<B1-Motion>",bMove, add='+')
    listbox.bind("<Shift-ButtonPress-1>",bDown_Shift, add='+')
    listbox.bind("<Shift-ButtonRelease-1>",bUp_Shift, add='+')
    root.mainloop()

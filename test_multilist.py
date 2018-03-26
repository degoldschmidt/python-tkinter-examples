from tkinter import *
<<<<<<< HEAD

class MultiListbox(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.lists = []
        for l, w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                 relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand'] = sb.set

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first, last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

=======
from tkinter import ttk
from tkinter.font import Font
from demopanels import MsgPanel, SeeDismissPanel
 
class MCListDemo(ttk.Frame):
     
    # class variable to track direction of column
    # header sort
    SortDir = True     # descending
         
    def __init__(self, isapp=True, name='mclistdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Multi-Column List Demo')
        self.isapp = isapp
        self._create_widgets()
         
    def _create_widgets(self):
        if self.isapp:
            MsgPanel(self,
                     [ "One of the new Ttk widgets is a tree widget ",
                      "which can be configured to display multiple columns of data without ",
                      "displaying the tree itself. This is a simple way to build a listbox that has multiple ",
                      "columns.\n\n",
                      "Click a column heading to re-sort the data. ",
                      "Drag a column boundary to resize a column."])
             
            SeeDismissPanel(self)
         
        self._create_demo_panel()
         
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
         
        self._create_treeview(demoPanel)
        self._load_data()
 
    def _create_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=TOP, fill=BOTH, expand=Y)
         
        # create the tree and scrollbars
        self.dataCols = ('country', 'capital', 'currency')       
        self.tree = ttk.Treeview(columns=self.dataCols,
                                 show = 'headings')
         
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
         
        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)
         
        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
         
    def _load_data(self):
         
        self.data = [
                ("Argentina",      "Buenos Aires",     "ARS"),
                ("Australia",      "Canberra",         "AUD"),
                ("Brazil",         "Brazilia",         "BRL"),
                ("Canada",         "Ottawa",           "CAD"),
                ("China",          "Beijing",          "CNY"),
                ("France",         "Paris",            "EUR"),
                ("Germany",        "Berlin",           "EUR"),
                ("India",          "New Delhi",        "INR"),
                ("Italy",          "Rome",             "EUR"),
                ("Japan",          "Tokyo",            "JPY"),
                ("Mexico",         "Mexico City",      "MXN"),
                ("Russia",         "Moscow",           "RUB"),
                ("South Africa",   "Pretoria",         "ZAR"),
                ("United Kingdom", "London",           "GBP"),
                ("United States",  "Washington, D.C.", "USD") ]
                 
        # configure column headings
        for c in self.dataCols:
            self.tree.heading(c, text=c.title(),
                              command=lambda c=c: self._column_sort(c, MCListDemo.SortDir))           
            self.tree.column(c, width=Font().measure(c.title()))
             
        # add data to the tree
        for item in self.data:
            self.tree.insert('', 'end', values=item)
             
            # and adjust column widths if necessary
            for idx, val in enumerate(item):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width = iwidth)
         
    def _column_sort(self, col, descending=False):
         
        # grab values to sort as a list of tuples (column value, column id)
        # e.g. [('Argentina', 'I001'), ('Australia', 'I002'), ('Brazil', 'I003')]
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
         
        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)   # item[1] = item Identifier
         
        # reverse sort direction for next sort operation
        MCListDemo.SortDir = not descending
         
>>>>>>> 5b8abb6130d95495bdae5945089775df55a5a8f2
if __name__ == '__main__':
    MCListDemo().mainloop()
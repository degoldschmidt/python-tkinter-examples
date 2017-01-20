from tkinter import *
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
         
if __name__ == '__main__':
    MCListDemo().mainloop()
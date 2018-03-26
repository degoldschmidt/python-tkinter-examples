from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog

d = [ 'Name',
      '# males',
      '# females',
      'Age males',
      'Age females',
      'Genotype',
      'Stimulus',
      'Temperature']

### This is for window
class App():
    def __init__ (self):
        self.Vars = []
        self.Categories = []
        self.listFlies = []
        self.root = self.makeWindow()
        self.setSelect ()
        self.root.mainloop()

    def makeWindow (self):
        root = Tk()
        root.title("Fly Logger v0.1")
        root.resizable(width=True, height=True)
        root.geometry("400x600")

        # create a menu
        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.restart)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save...")
        filemenu.add_separator()
        filemenu.add_command(label="Import...")
        filemenu.add_command(label="Export...")
        filemenu.add_separator()
        filemenu.add_command(label="Exit")

        viewmenu = Menu(menu)
        menu.add_cascade(label="View", menu=viewmenu)
        viewmenu.add_command(label="View experiment")
        viewmenu.add_command(label="View history")

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...")

        frame1 = Frame(root)
        frame1.pack()

        Label(frame1, text="Please type in information about experimental run").grid(row=0, column = 0,  columnspan=2, sticky=W+E, pady=2)
        for ind, cats in enumerate(d):
            self.addCategory(frame1, cats, ind)

        frame2 = Frame(root)       # Row of buttons
        frame2.pack()
        b1 = Button(frame2,text=" Add  ",command=self.addEntry)
        #b2 = Button(frame2,text=" Load ",command=loadEntry)
        b3 = Button(frame2,text="Delete",command=self.deleteEntry)
        b4 = Button(frame2,text=" Edit ",command=self.updateEntry)
        b1.pack(side=LEFT)
        b3.pack(side=LEFT)
        b4.pack(side=LEFT)

        frame3 = Frame(root)       # select of names
        frame3.pack()
        scroll = Scrollbar(frame3, orient=VERTICAL)
        self.select = Listbox(frame3, yscrollcommand=scroll.set, height=12)
        self.select.bind('<Double-Button-1>', self.doubleClicked)
        scroll.config (command=self.select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.select.pack(side=LEFT,  fill=BOTH, expand=1)

        frame4 = Frame(root)
        frame4.pack()


        return root

    def restart (self):
        self.listFlies = []
        self.Vars = []
        self.Categories = []
        self.setSelect()
        self.root.destroy()
        self.root = self.makeWindow()

    def open_file(self):
        name= filedialog.askopenfilename()
        print(name)

    def save_file(self):
        print("Yeah")

    def doubleClicked (self, event) :
        self.loadEntry()

    def whichSelected (self) :
        if len(self.select.curselection()) > 0:
            return int(self.select.curselection()[0])
        else:
            print("Warning: No entry selected.")
            return None

    def addCategory (self, frame, title, ind):
        Label(frame, text=title).grid(row=ind+1, column=0, sticky=W, pady=1)
        self.Vars.append(StringVar())
        self.Categories.append(Entry(frame, textvariable=self.Vars[-1]))
        self.Categories[-1].grid(row=ind+1, column=1, sticky=W, pady=1)

    def addEntry (self):
        temp = []
        for var in self.Vars:
            temp.append(var.get())
        fly = Fly(temp)
        self.listFlies.append(fly)
        self.setSelect ()

    def updateEntry (self):
        for ind, var in enumerate(self.Vars):
            self.listFlies[self.whichSelected()].set(ind, var.get())
        setSelect ()

    def deleteEntry (self):
        if self.whichSelected() == None:
            print("")
        else:
            del self.listFlies[self.whichSelected()]
        self.setSelect ()

    def loadEntry (self):
        for ind, var in enumerate(self.Vars):
            temp = self.listFlies[self.whichSelected()].get(ind)
            var.set(temp)

    def setSelect (self) :
        self.select.delete(0,END)
        for ind, fly in enumerate(self.listFlies):
            self.select.insert (END, "{:03}".format(ind+1) + "\t\t" + fly.get(0))

class Fly:
    def __init__(self, indata):
        self.data = []
        for vals in indata:
            self.data.append(vals)

    def get(self, ind):
        return self.data[ind]

    def set(self, ind, val):
        self.data[ind] = val

def main():
    app = App()
    app.root.mainloop()

if __name__ == '__main__':
    main()

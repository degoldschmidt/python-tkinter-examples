from tkinter import *
from tkinter import messagebox

listFlies = []
d = [ 'Name', 
      '# males', 
      '# females',
      'Age males',
      'Age females',
      'Genotype',
      'Stimulus',
      'Temperature']

### This is for window
Vars = []
Categories = []

class Fly:
    data = []
    def __init__(self, indata):
        for vals in indata:
            self.data.append(vals)
        
    def get(self, ind):
        return self.data[ind]
    
    def set(self, ind, val):
        self.data[ind] = val
        
def doubleClicked (event) : 
    loadEntry()   

def whichSelected () :
    #print("At %s of %d" % (select.curselection(), len(listFlies)))
    if len(select.curselection()) > 0:
        return int(select.curselection()[0])
    else:
        print("No experiment selected")
        return None

def addCategory (frame, title, ind):
    Label(frame, text=title).grid(row=ind+1, column=0, sticky=W, pady=1)
    Vars.append(StringVar())
    Categories.append(Entry(frame, textvariable=Vars[-1]))
    Categories[-1].grid(row=ind+1, column=1, sticky=W, pady=1)

def addEntry () :
    #print(Vars[0], Vars[0].get())
    fly = Fly((Vars[0].get(), Vars[1].get(), Vars[2].get(), Vars[3].get(), Vars[4].get(), Vars[5].get()))
    listFlies.append(fly)
    setSelect ()

def updateEntry() :
    listFlies[whichSelected()].setName(Vars[0].get())
    listFlies[whichSelected()].setGenotype(Vars[1].get())
    setSelect ()

def deleteEntry() :
    if whichSelected() == None:
        print("")
    else:
        del listFlies[whichSelected()]
    setSelect ()

def loadEntry  () :
    name = listFlies[whichSelected()].getName()
    geno = listFlies[whichSelected()].getGenotype()
    Vars[0].set(name)
    Vars[1].set(geno)

def makeWindow () :
    global name, gender, age, genotype, stimulus, temperature, select
    root = Tk()
    root.title("Fly Logger v0.1")
    root.resizable(width=True, height=True)
    root.geometry("400x600")
    
    # create a menu
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open...")
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
        addCategory(frame1, cats, ind)

    frame2 = Frame(root)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2,text=" Add  ",command=addEntry)
    b2 = Button(frame2,text="Update",command=updateEntry)
    b3 = Button(frame2,text="Delete",command=deleteEntry)
    b4 = Button(frame2,text=" Load ",command=loadEntry)
    b1.pack(side=LEFT); b2.pack(side=LEFT)
    b3.pack(side=LEFT); b4.pack(side=LEFT)

    frame3 = Frame(root)       # select of names
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=12)
    select.bind('<Double-Button-1>', doubleClicked)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    return root

def setSelect () :
    #listFlies.sort(key=lambda fly: fly.name)
    #print(listFlies)
    select.delete(0,END)
    for ind, fly in enumerate(listFlies):
        select.insert (END, "{:03}".format(ind) + "\t\t" + fly.get(0))

root = makeWindow()
setSelect ()
root.mainloop()

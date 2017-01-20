import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
import networkx as nx
from tkinter import messagebox
import math


class App():
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("Animated Graph embedded in TK")
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.root.resizable(width=True, height=True)
        self.root.geometry("800x400")
        self.colors = ['#B2E4CF', '#E4E4B2']
        
        # the networkx part
        self.G = List()
        
        # figure
        self.f = plt.figure(figsize=(5,4))
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.show()
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        # axes    
        self.a = self.f.add_subplot(111)
        self.pos = (1, 1)
        self.draw()
        

    def update(self):
        self.root.mainloop()
    
    def quit_app(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            
    def draw(self):
        self.a.cla()
        nx.draw_networkx(self.G.getGraph(), self.G.getPos(), ax=self.a, with_labels=True, node_color= self.G.getColors(), node_size=1000)
        self.a.plot(self.pos[0], self.pos[1], 'r.')
        plt.axis('off')
        self.a.set_xlim(0,1)
        self.a.set_ylim(0,1)
        plt.tight_layout()
        self.canvas.draw()
        
    def closeEntryWindow(self):
        self.entryWindow.destroy()
    
    def openEntryWindow(self, x, y):
        self.pos = (x, y)
        self.draw()
        self.entryWindow = Tk()
        self.entryWindow.wm_title("Type in node details")
        self.entryWindow.protocol("WM_DELETE_WINDOW", self.closeEntryWindow)

        Label(self.entryWindow, text="Genotype").grid(row=0, column=0, sticky=W, pady=1)
        self.genentry = Entry(self.entryWindow)
        self.genentry.grid(row=0, column=1, sticky=W, pady=1)
        self.genentry.bind("<Return>",self.Enter)
        Label(self.entryWindow, text="Date").grid(row=1, column=0, sticky=W, pady=1)
        self.datentry = Entry(self.entryWindow)
        self.datentry.grid(row=1, column=1, sticky=W, pady=1)
        self.datentry.bind("<Return>",self.Enter)

    def Enter(self,event):
        name = self.genentry.get()
        date = self.datentry.get()
        print(name, date)
        self.G.addNode(name, self.pos, self.colors[0], date)
        self.draw()
        self.entryWindow.destroy()
        
    def on_press(self, event):
        if event.xdata is not None and event.ydata is not None:
        #print('you pressed', event.button, event.xdata, event.ydata)
            if not self.G.isNear((event.xdata, event.ydata), self.getScale(self.f.gca().get_xlim(), self.f.gca().get_ylim())):
                self.openEntryWindow(event.xdata, event.ydata)
                
    def getScale(self, x, y):
        return (x[1]-x[0],y[1]-y[0])
                
        
            
class List():
    def __init__(self):
        self.Graph = nx.Graph()
        self.Nodes = []
        
    def addNode(self, Name, Pos, Color, Date):
        self.Graph.add_node(self.getMask(Name, Date), pos=Pos)
        node = Node(Name, Pos, Color, Date)
        self.Nodes.append(node)
        self.Nodes.sort(key = lambda c: c.name)
    
    def getColors(self):
        colors = []
        for node in self.Graph.nodes():
            newnode = self.getNode(node)
            colors.append(newnode.C())
        return colors   
        
    def getGraph(self):
        return self.Graph
    
    def getMask(self, Name, Date):
        return "\n\n" + Name + "\n\n" + Date
    
    def getNode(self, Name):
        for node in self.Nodes:
            if Name == self.getMask(node.N(),node.D()):
                return node
        return None
    
    def getPos(self):
        return nx.get_node_attributes(self.Graph, 'pos')
    
    def len(self):
        return len(self.Graph)
    
    def isNear(self, Pos, Scale):
        distance = 0.0
        print(Scale)
        for node in self.Nodes:
            print("dx: %f" % (node.x()-Pos[0]))
            print("dy: %f" % (node.y()-Pos[1]))
            distance = ((node.x()-Pos[0])/Scale[0])**2 + ((node.y()-Pos[1])/Scale[1])**2
            distance = math.sqrt(distance)
            #if distance < 0.0333:
            #    return True 
        return False
        #for node in getNodes

class Node():
    def __init__(self, Name, Pos, Color, Date):
        self.name = Name
        self.pos = Pos
        self.color = Color
        self.date = Date
    
    def C(self):
        return self.color
    
    def D(self):
        return self.date
    
    def N(self):
        return self.name
    
    def x(self):
        return self.pos[0]
    
    def y(self):
        return self.pos[1]

if __name__ == '__main__':

    myApp = App()
    myApp.update()
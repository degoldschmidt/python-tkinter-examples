from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import sys

print(sys.platform)

root = Tk()
image = Image.open('icon/icon.png').convert("RGBA")
image = image.resize((100,100), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
photo = PhotoImage(file='icon/datasets.gif')
if sys.platform == 'darwin':
    s = Style()
    s.configure('TNotebook', tabposition='nw')
    s.configure('TNotebook.Tab', padding=(20, 8, 20, 0))

note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
Button(tab1, text='Exit', command=root.destroy).pack(padx=10, pady=10)
label = Label(root, image=photo)
label.image = photo # keep a reference!
label.pack()


note.add(tab1, text=    "      Tab One      ")
note.add(tab2, text =   "      Tab Two      ")
note.add(tab3, text =   "     Tab Three     ")
note.pack(fill=BOTH,expand=1)

root.mainloop()
#exit()

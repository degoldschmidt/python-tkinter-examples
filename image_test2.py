from tkinter import *
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk

root = Tk()
root.geometry("")

file = BytesIO(urllib.request.urlopen('http://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png').read())
img = Image.open(file)

photo = ImageTk.PhotoImage(img)
xxx= Label(root, image = photo)      # Not working in Mac
# xxx= Button(root, image = photo)   # This works in Mac
xxx.grid(row=14, column=0, rowspan = 5)
# img.show()        # opens perfectly using 'Preview' application in Mac

root.mainloop()

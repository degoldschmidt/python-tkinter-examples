import tkinter as Tk
import tkinter.ttk as ttk
import tkinter.font as font
import time as t

def update_bg():
    

root = Tk.Tk()
# make it cover the entire screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.focus_set()

### STYLE
# fonts
helvneue24 = font.Font(family='Helvetica Neue Light', size=24, weight='normal')

# colors
hour = int(t.strftime("%S", t.localtime()))
bgcols =   ["#22A7F0", "#23ABEA", "#25AFE5", "#27B4E0", "#29B8DB", "#2BBCD6", "#2CC1D0", "#2EC5CB", "#30C9C6", "#32CEC1", "#34D2BC", "#36D7B7"]
if (hour-9) < 0 or (hour-9)>(len(bgcols)-1):
    current_bg = "#22313F"  ### nighttime color
else:
    current_bg = bgcols[hour-9]
root.configure(background=current_bg)
ttk.Style().configure('green/black.TButton', foreground=current_bg, background=current_bg, font=helvneue24, bd=5)

root.call("::tk::unsupported::MacWindowStyle", "style", root, "plain", "none")
root.attributes("-fullscreen",True)
root.wm_attributes("-topmost", True)
root.wm_state("zoomed")



button = ttk.Button(root, text="Click me!", style='green/black.TButton')
#img = PhotoImage(file="C:/path to image/example.gif") # make sure to add "/" not "\"
#button.config()
button.place(relx=0.5, rely=0.5, anchor = Tk.CENTER) # Displaying the button

root.after(1000, update_bg)
root.mainloop()

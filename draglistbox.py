import tkinter as tk

class Drag_and_Drop_Listbox(tk.Listbox):
  """ A tk listbox with drag'n'drop reordering of entries. """
  def __init__(self, master, **kw):
    kw['selectmode'] = tk.MULTIPLE
    kw['activestyle'] = 'none'
    tk.Listbox.__init__(self, master, kw)
    self.bind('<Button-1>', self.getState, add='+')
    self.bind('<Button-1>', self.setCurrent, add='+')
    self.bind('<B1-Motion>', self.shiftSelection)
    self.curIndex = None
    self.curState = None
  def setCurrent(self, event):
    ''' gets the current index of the clicked item in the listbox '''
    self.curIndex = self.nearest(event.y)
  def getState(self, event):
    ''' checks if the clicked item in listbox is selected '''
    i = self.nearest(event.y)
    self.curState = self.selection_includes(i)
  def shiftSelection(self, event):
    ''' shifts item up or down in listbox '''
    i = self.nearest(event.y)
    if self.curState == 1:
      self.selection_set(self.curIndex)
    else:
      self.selection_clear(self.curIndex)
    if i < self.curIndex:
      # Moves up
      x = self.get(i)
      selected = self.selection_includes(i)
      self.delete(i)
      self.insert(i+1, x)
      if selected:
        self.selection_set(i+1)
      self.curIndex = i
    elif i > self.curIndex:
      # Moves down
      x = self.get(i)
      selected = self.selection_includes(i)
      self.delete(i)
      self.insert(i-1, x)
      if selected:
        self.selection_set(i-1)
      self.curIndex = i

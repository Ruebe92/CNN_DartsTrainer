## Imports
import tkinter as tk
from matplotlib import colors as mcolors

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


class Label:
    
    def __init__(self, parent, row, column, text):
        
        label = tk.Label(parent, text = text)
        label.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        label.config(font=('verdana', 12))

class Button(tk.Button):
    
    def __init__(self, parent, row, column,rowspan, columnspan, text):
        
        super().__init__(parent, text = text)
        
        self.grid(row=row, column = column, rowspan = rowspan, columnspan = columnspan, padx=(5, 5), pady=(5,5))
        self.config(font=('verdana', 10))
                

class Entry(tk.Entry):
    
    def __init__(self, parent, row, column, color):
        
        super().__init__(parent)
        
        self.insert(0,"0.00")
        self.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        self.config(font=('verdana', 12), justify='right', borderwidth=1, relief="solid", width = 10, bg = color)
        
    def reset(self):
        
        self.delete(0,20)
        self.insert(0,str("0.00"))


class Table:
    
    def __init__(self, parent, width, height, row, column):
        
        table = tk.Frame(parent, width = 390, height = 200)  
        table.grid(row = 0, column = 0, rowspan = 4, columnspan = 4, padx = (20,0))
        table.grid_propagate(0)
        
        
        label_dart = Label(table,0,0,"Dart")
        label_X = Label(table,0,1,"X")
        label_Y = Label(table,0,2,"Y")
        label_dart1 = Label(table, 1, 0, "1")
        label_dart2 = Label(table, 2, 0,"2")
        label_dart3 = Label(table, 3, 0,"3")
        
        self.entry_dart1_X = Entry(table, 1, 1, colors["deepskyblue"])
        self.entry_dart2_X = Entry(table, 2, 1, colors["orangered"])
        self.entry_dart3_X = Entry(table, 3, 1, colors["darkmagenta"])
        
        self.entry_dart1_Y = Entry(table, 1, 2, colors["deepskyblue"])
        self.entry_dart2_Y = Entry(table, 2, 2, colors["orangered"])
        self.entry_dart3_Y = Entry(table, 3, 2, colors["darkmagenta"])
        
        
        
    def reset(self):
            
            #Reset table
            self.entry_dart1_X.reset()
            self.entry_dart1_Y.reset()
            
            self.entry_dart2_X.reset()
            self.entry_dart2_Y.reset()
            
            self.entry_dart3_X.reset()
            self.entry_dart3_Y.reset()
            
           

class Frame(tk.Frame): 

    
    def __init__(self, parent, width, height, row, column):
        
        super().__init__(parent)
        
        self.config( width = 640, height = 100)
        self.grid(row=3, column=0, rowspan = 2)
        

        self.table = Table(self, 390, 200, 0, 0)
        
        self.button_reset = Button(self,0, 5, 1, 1, "Reset Values")
        self.button_reset.config(command = parent.reset, bg = "red",width = 12, height = 2)
        
        self.button_cancel = Button(self,0, 6, 1, 1, "Cancel Throwing")
        self.button_cancel.config(bg = "red",width = 12, height = 2)
        
        self.button_delete_and_next = Button(self,1, 5, 2, 1, "Delete & \n Next Throw")
        self.button_delete_and_next.config(bg = "red",width = 12, height = 6, state = "normal")
        
        self.button_save_and_next = Button(self,1, 6, 2, 1, "Save & \n Next Throw")
        self.button_save_and_next.config(command = parent.next_throw, bg = "green", width = 12, height = 6, state = "disabled")
        
        

        
        
        
        
#%%
### Own imports
import dartboard
import dartshelper as dh

### Other
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import time


class dartsGUI:
    
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            print (round(event.xdata,2), round(event.ydata,2))
            
            self.X.insert(0,str(round(event.xdata,2)))
            
            
            
        else:
            
            print ('Clicked ouside axes bounds but inside plot window')
    
    
    def __init__(self, window, window_title):
    
        window.resizable(0, 0)
    
        fig, ax = dartboard.Draw_Dartboard()
        
        self.boardCanvas = FigureCanvasTkAgg(fig, master=window)
        self.boardCanvas.get_tk_widget().config(width=640, height=640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, )
        self.boardCanvas.draw()
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
        
        self.X = tk.Entry(window, text="Yes, yes yaw")
        self.X.insert(0,"Waiting for user...")
        self.X.grid(row=1, column=0)
        
        self.X = tk.Entry(window, text="Yes, yes yaw")
        self.X.insert(0,"Waiting for user...")
        self.X.grid(row=1, column=0)
        
        plt.close('all')
        
        self.window = window
        self.window.title(window_title)
                
        self.window.mainloop()



if __name__ == "__main__":
    
    
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP")
    
    



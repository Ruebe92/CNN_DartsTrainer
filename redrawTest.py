#%%
### Own imports
import dartboard
import testGUI as tg
#import dartshelper as dh

### Other
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class dartsGUI:

    def on_click(self,event):
        
        #self.ax.clear()
        
        #self.fig, self.ax = dartboard.Draw_Dartboard()
        #self.boardCanvas = FigureCanvasTkAgg(self.fig, master= self.window)
        
        self.ax.plot(event.xdata, event.ydata, "+")
        
        self.boardCanvas.draw()
        
        if event.inaxes is not None:
            
            #self.boardCanvas.create_oval(10, 10, 20, 20, width=2, fill='blue')
            
            
            print( str(round(event.xdata,2)) + "  " + str(round(event.ydata,2)))
            
        
        else:
            
            print ('Clicked ouside axes bounds but inside plot window')
    
    def create_board_canvas(self):
        
        self.fig, self.ax = dartboard.Draw_Dartboard()
        
        self.boardCanvas = FigureCanvasTkAgg(self.fig, master= self.window)
        self.boardCanvas.get_tk_widget().config(width = 640, height = 640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, )
        
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
        #plt.show()
        plt.close('all')
    
    

    def __init__(self, window, window_title):
        
            window.geometry("1280x840")    
            
            window.resizable(0, 0)
            
            self.window = window
            
            self.window.title(window_title)
        
            self.create_board_canvas()
            
            self.window.mainloop()
            
            

if __name__ == "__main__":
    
    
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP")
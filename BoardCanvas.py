## Imports
import tkinter as tk
import dartboard 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BoardCanvas:
    
    def __init__(self, parent, width, height, row, column, main):
         
        self.main = main
    
        fig_board, ax_board = dartboard.Draw_Dartboard()
        
        boardCanvas = FigureCanvasTkAgg(fig_board, master = parent)
        
        plt.close('all')
       
        boardCanvas.get_tk_widget().config(width = width, height = height, cursor="target")
        
        boardCanvas.get_tk_widget().grid(row=0, column=0, rowspan = 3)
        
        boardCanvas.mpl_connect('button_press_event', self.on_click)
        
        
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            self.main.frame_UI_left.table.enter_value(round(event.xdata,3),round(event.ydata,3))
            
            if self.main.frame_UI_left.table.focus < 2:
                
                self.main.frame_UI_left.table.focus += 1
                self.main.frame_UI_left.table.change_table_focus()
            
            #Draw Cross
            #self.ax_board.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["deepskyblue"])
            #self.boardCanvas.draw()
        
        else:
            
            print ('Clicked ouside axes bounds but inside plot window')
        
        
    def reset(self):
        
        print("Dummy. Darboard will be reset")
            
        
        

        
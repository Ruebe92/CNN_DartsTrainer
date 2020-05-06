## Imports
import tkinter as tk
import dartboard 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors as mcolors

class BoardCanvas:
    
    def __init__(self, parent, width, height, row, column, main):
         
        self.main = main
        self.markers = []
        self.dart = 0
        
        fig, self.ax = dartboard.Draw_Dartboard()
        
        self.boardCanvas = FigureCanvasTkAgg(fig, master = parent)
        
        plt.close('all')
       
        self.boardCanvas.get_tk_widget().config(width = width, height = height, cursor="target")
        
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, rowspan = 3)
        
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            x = round(event.xdata,3)
            y = round(event.ydata,3)
            
            # Send click data to table
            self.main.frame_UI_left.table.on_click(x,y)

            # Draw marker
            if self.dart < 3:            
                
                self.draw_marker(round(event.xdata,3),round(event.ydata,3), self.dart)
                
                self.dart += 1
                
            else:
                
                
                #Remove last marker from list and remove marker from plot
                self.markers.pop().remove()
                #Draw new marker
                self.draw_marker(round(event.xdata,3),round(event.ydata,3), 2)
            
            self.boardCanvas.draw()
            
        
        else:
            
            self.main.text_display.print_to_display("User has clicked outside the canvas...")
      
    def draw_marker(self, x, y, int_color):
        
        ln, = self.ax.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.main.dart_colors[int_color])
        
        self.markers.append(ln)

        
    def reset(self):
        
        if len(self.markers) != 0: 
        
            for marker in self.markers:
                
                marker.remove()
                
                
        self.markers = []
        self.dart = 0
        self.boardCanvas.draw()
        
        self.main.text_display.print_to_display("Board has been cleared!")
            
        
        

        
#%%
### Own imports
import dartboard
#import dartshelper as dh
import time

### Other
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class dartsGUI:
    
###-------------Functionality---------------    
    
    def set_table_focus(self,focus):
        
        if focus == 1:
            
            self.entry_dart1_X.config(borderwidth = 3)
            self.entry_dart1_Y.config(borderwidth = 3)
            self.entry_dart2_X.config(borderwidth = 1)
            self.entry_dart2_Y.config(borderwidth = 1)
            self.entry_dart3_X.config(borderwidth = 1)
            self.entry_dart3_Y.config(borderwidth = 1)
            
        elif focus == 2:
            
            self.entry_dart1_X.config(borderwidth = 1)
            self.entry_dart1_Y.config(borderwidth = 1)
            self.entry_dart2_X.config(borderwidth = 3)
            self.entry_dart2_Y.config(borderwidth = 3)
            self.entry_dart3_X.config(borderwidth = 1)
            self.entry_dart3_Y.config(borderwidth = 1)
            
        elif focus == 3:
            
            self.entry_dart1_X.config(borderwidth = 1)
            self.entry_dart1_Y.config(borderwidth = 1)
            self.entry_dart2_X.config(borderwidth = 1)
            self.entry_dart2_Y.config(borderwidth = 1)
            self.entry_dart3_X.config(borderwidth = 3)
            self.entry_dart3_Y.config(borderwidth = 3)
            
            
    def enter_value_focus(self, x, y, focus):
        
        if focus == 1:
            
            #Draw Cross
            self.ax.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["deepskyblue"])
            self.boardCanvas.draw()
            
            ##Entry
            self.entry_dart1_X.delete(0,20)
            self.entry_dart1_X.insert(0,str(x))
            self.entry_dart1_Y.delete(0,20)
            self.entry_dart1_Y.insert(0,str(y))
              
        elif focus == 2:
            
            #Draw Cross
            self.ax.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["orangered"])
            self.boardCanvas.draw()
            
            self.entry_dart2_X.delete(0,20)
            self.entry_dart2_X.insert(0,str(x))
            self.entry_dart2_Y.delete(0,20)
            self.entry_dart2_Y.insert(0,str(y))
            
        elif focus == 3:
            
            #Draw Cross
            self.ax.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["darkmagenta"])
            self.boardCanvas.draw()
            
            
            self.entry_dart3_X.delete(0,20)
            self.entry_dart3_X.insert(0,str(x))
            self.entry_dart3_Y.delete(0,20)
            self.entry_dart3_Y.insert(0,str(y))
        
        
        
    
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            
            self.enter_value_focus(round(event.xdata,3),round(event.ydata,3), self.dart_count)
            
            self.dart_count = self.dart_count + 1
            
            self.set_table_focus(self.dart_count)
        
        else:
            
            print ('Clicked ouside axes bounds but inside plot window')
            
    def reset(self):
            
            #Reset table
            self.entry_dart1_X.delete(0,20)
            self.entry_dart1_X.insert(0,str("0.00"))
            self.entry_dart1_Y.delete(0,20)
            self.entry_dart1_Y.insert(0,str("0.00"))
            
            self.entry_dart2_X.delete(0,20)
            self.entry_dart2_X.insert(0,str("0.00"))
            self.entry_dart2_Y.delete(0,20)
            self.entry_dart2_Y.insert(0,str("0.00"))
            
            self.entry_dart3_X.delete(0,20)
            self.entry_dart3_X.insert(0,str("0.00"))
            self.entry_dart3_Y.delete(0,20)
            self.entry_dart3_Y.insert(0,str("0.00"))

            self.dart_count = 1
            self.set_table_focus(self.dart_count)
            
            #Reset darboard
            self.boardCanvas.get_tk_widget().grid_remove()
            self.create_board_canvas()
            
    def print_to_display(self,message):
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        statement = "\n[{0}]: {1}".format(current_time,message)
        
        self.text_display.insert(tk.END, statement)
        self.text_display.see("end")
        
        
            
###-------------GUI-Creation--------------- 
# Frames and widgets are created from top to bottom and from left to right!


    def create_board_canvas(self):
        
        self.fig, self.ax = dartboard.Draw_Dartboard()
        mng = plt.get_current_fig_manager()
        mng.window.showMinimized()
        self.boardCanvas = FigureCanvasTkAgg(self.fig, master= self.window)
        
        plt.close('all')
       
        self.boardCanvas.get_tk_widget().config(width = 640, height = 640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, )
        
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)

        
    def create_display_frame(self):
        
        self.text_display = tk.Text(root, height= 10, width = 65, relief="solid", borderwidth=1)
        self.text_display.grid(row=1, column=1, padx = (50,0))
        self.print_to_display("Application started...")
        self.print_to_display("Waiting for user input...")
        
        
        for x in range(54):
            
            self.print_to_display(str(x))
        
    
    def create_UI_frame(self):
        
        ## UI
        self.UIFrame = tk.Frame(self.window, width = 640, height = 100)
        #self.UIFrame.grid_propagate(0)
        self.UIFrame.grid(row=1, column=0)

        self.create_table()
        
        self.button_reset = self.create_button(self.UIFrame,0, 5, 1, 1, "Reset Values")
        self.button_reset.config(command = self.reset, bg = "red",width = 12, height = 2)
        
        self.button_delete = self.create_button(self.UIFrame,0, 6, 1, 1, "Delete Throws")
        self.button_delete.config(bg = "red",width = 12, height = 2)
        
        self.button_delete_and_next = self.create_button(self.UIFrame,1, 5, 2, 1, "Delete & \n Next Throw")
        self.button_delete_and_next.config(bg = "red",width = 12, height = 6)
        
        self.button_save_and_next = self.create_button(self.UIFrame,1, 6, 2, 1, "Save & \n Next Throw")
        self.button_save_and_next.config(bg = "green", width = 12, height = 6)
        
         
    def create_button(self, parent, row, column,rowspan, columnspan, text):
        button = tk.Button(parent, text = text)
        button.grid(row=row, column = column, rowspan = rowspan, columnspan = columnspan, padx=(5, 5), pady=(5,5))
        button.config(font=('verdana', 10))
        
        return button
        
        
    def create_table(self):
        
        ## Table
        table = tk.Frame(self.UIFrame, width = 390, height = 200)  
        table.grid(row = 0, column = 0, rowspan = 4, columnspan = 4, padx = (20,0))
        table.grid_propagate(0)
        
        
        label_dart = self.create_table_label(table,0,0,"Dart")
        label_X = self.create_table_label(table,0,1,"X")
        label_Y = self.create_table_label(table,0,2,"Y")
        label_dart1 = self.create_table_label(table, 1, 0, "1")
        label_dart2 = self.create_table_label(table, 2, 0,"2")
        label_dart3 = self.create_table_label(table, 3, 0,"3")
        
        
        
        self.entry_dart1_X = self.create_tabel_entry(table, 1, 1, self.colors["deepskyblue"])
        self.entry_dart2_X = self.create_tabel_entry(table, 2, 1, self.colors["orangered"])
        self.entry_dart3_X = self.create_tabel_entry(table, 3, 1, self.colors["darkmagenta"])
        
        self.entry_dart1_Y = self.create_tabel_entry(table, 1, 2, self.colors["deepskyblue"])
        self.entry_dart2_Y = self.create_tabel_entry(table, 2, 2, self.colors["orangered"])
        self.entry_dart3_Y = self.create_tabel_entry(table, 3, 2, self.colors["darkmagenta"])
        
        
        
    def create_table_label(self,parent, row, column, text):
        
        label = tk.Label(parent, text = text)
        label.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        label.config(font=('verdana', 12))
        
        return label
        
    
        
    def create_tabel_entry(self, parent, row, column, color):
        
        entry = tk.Entry(parent, justify='right', borderwidth=1, relief="solid", width = 10, bg = color)
        entry.insert(0,"0.00")
        entry.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        entry.config(font=('verdana', 12))
        
        return entry
    
    def create_video_frame(self):
        
        ## Video
        videoFrame = tk.Frame(self.window, bg = "green")
        videoFrame.grid(row=0, column=1, rowspan = 2, columnspan = 1)
        videoFrame.grid_propagate(0)
        
        self.videoCanvasTop = tk.Canvas(videoFrame, width = 320, height = 180, bg = "black")
        self.videoCanvasTop.grid(row=0,column=0)
        self.videoCanvasRight = tk.Canvas(videoFrame,width= 320, height= 180, bg = "blue")
        self.videoCanvasRight.grid(row=0,column=1)
        
    
    def __init__(self, window, window_title):
    
        window.geometry("1280x840")    
        
        window.resizable(0, 0)
        
        self.colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        
        self.window = window
        
        self.window.title(window_title)
    
        self.create_board_canvas()
        
        self.create_UI_frame()
        
        
        
        self.create_video_frame()
        
        self.dart_count = 1
        self.set_table_focus(self.dart_count)
        
        self.create_display_frame()
        
        
                
        self.window.mainloop()


if __name__ == "__main__":
    
    
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP")
    
    



#%%
### Own imports
import dartboard
#import dartshelper as dh

### Other
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class dartsGUI:
    
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
            
            self.entry_dart1_X.delete(0,20)
            self.entry_dart1_X.insert(0,str(x))
            self.entry_dart1_Y.delete(0,20)
            self.entry_dart1_Y.insert(0,str(y))
              
        elif focus == 2:
            
            self.entry_dart2_X.delete(0,20)
            self.entry_dart2_X.insert(0,str(x))
            self.entry_dart2_Y.delete(0,20)
            self.entry_dart2_Y.insert(0,str(y))
            
        elif focus == 3:
            
            self.entry_dart3_X.delete(0,20)
            self.entry_dart3_X.insert(0,str(x))
            self.entry_dart3_Y.delete(0,20)
            self.entry_dart3_Y.insert(0,str(y))
        
        
        
    
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            #self.boardCanvas.create_oval(10, 10, 20, 20, width=2, fill='blue')
            
            
            self.enter_value_focus(round(event.xdata,2),round(event.ydata,2), self.dart_count)
            
            self.dart_count = self.dart_count + 1
            
            self.set_table_focus(self.dart_count)
        
        else:
            
            print ('Clicked ouside axes bounds but inside plot window')
    
    def create_board_canvas(self):
        
        fig, ax = dartboard.Draw_Dartboard()
        
        self.boardCanvas = FigureCanvasTkAgg(fig, master= self.window)
        self.boardCanvas.get_tk_widget().config(width = 640, height = 640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, )
        
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
        #plt.show()
        plt.close('all')
    
    def create_UI_frame(self):
        
        ## UI
        self.UIFrame = tk.Frame(self.window, width = 640, height = 200)
        self.UIFrame.grid_propagate(0)
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
        
        
        
    def reset(self):
        
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
        
        
        
        self.entry_dart1_X = self.create_tabel_entry(table, 1, 1)
        self.entry_dart2_X = self.create_tabel_entry(table, 2, 1)
        self.entry_dart3_X = self.create_tabel_entry(table, 3, 1)
        
        self.entry_dart1_Y = self.create_tabel_entry(table, 1, 2)
        self.entry_dart2_Y = self.create_tabel_entry(table, 2, 2)
        self.entry_dart3_Y = self.create_tabel_entry(table, 3, 2)
        
        
        
    def create_table_label(self,parent, row, column, text):
        
        label = tk.Label(parent, text = text)
        label.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        label.config(font=('verdana', 12))
        
        return label
        
    
        
    def create_tabel_entry(self, parent, row, column):
        
        entry = tk.Entry(parent, justify='right', borderwidth=1, relief="solid", width = 10)
        entry.insert(0,"0.00")
        entry.grid(row=row, column=column, padx=(10, 10), pady=(10,10))
        entry.config(font=('verdana', 12))
        
        return entry
    
    def create_video_frame(self):
        
        ## Video
        videoFrame = tk.Frame(self.window, bg = "green", width = 640, height = 840)
        videoFrame.grid(row=0, column=1, rowspan = 2, columnspan = 1)
        videoFrame.grid_propagate(0)
        
        self.videoCanvasTop = tk.Canvas(videoFrame, width = 320, height = 180, bg = "black")
        self.videoCanvasTop.grid(row=0,column=0)
        self.videoCanvasRight = tk.Canvas(videoFrame,width= 320, height= 180, bg = "blue")
        self.videoCanvasRight.grid(row=0,column=1)
        
    
        
        
    
    
    def __init__(self, window, window_title):
    
        window.geometry("1280x840")    
        
        window.resizable(0, 0)
        
        self.window = window
        
        self.window.title(window_title)
    
        self.create_board_canvas()
        
        self.create_UI_frame()
        
        self.create_video_frame()
        
        self.dart_count = 1
        self.set_table_focus(self.dart_count)
        
       
        
        
                
        self.window.mainloop()
        
        
        
    
        
        



if __name__ == "__main__":
    
    
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP")
    
    



## Imports
import time

import tkinter as tk
import ttk as ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors as mcolors

import Darts_Helper as dh

class Frame(tk.Frame): 

    def __init__(self, parent, width, height, row, column, main):
        
        super().__init__(parent)
        
        self.config(width = width, height = height)
        self.grid(row = row, column = column)
        self.main = main
                    

class Frame_UI_Left(Frame):
    
    def __init__(self, parent, width, height, row, column, main):
        
        super().__init__(parent, width, height, row, column, main)
        
        
        self.table = Table(self, 390, 200, 0, 0, main)
        
        self.button_reset = Button(self,0, 5, 1, 1, "Reset Values")
        self.button_reset.config(command = main.reset, bg = "red",width = 12, height = 2)
    
        self.button_cancel = Button(self,0, 6, 1, 1, "Cancel Throwing")
        self.button_cancel.config(bg = "red",width = 12, height = 2)
        
        self.button_delete_and_next = Button(self,1, 5, 2, 1, "Delete & \n Next Throw")
        self.button_delete_and_next.config(command = main.del_and_next, bg = "red",width = 12, height = 6, state = "normal")
        
        self.button_save_and_next = Button(self,1, 6, 2, 1, "Save & \n Next Throw")
        self.button_save_and_next.config(command = main.save_and_next, bg = "green", width = 12, height = 6)

class Frame_UI_Right(Frame):
    
    def __init__(self, parent, width, height, row, column, main):
        
        super().__init__(parent, width, height, row, column, main)
       
        self.config(relief = "solid", borderwidth=1)

        self.grid(row=0, column=1, sticky = tk.N)
        
        label_ip = tk.Label(self, text="Video Address:")
        label_ip.grid(row = 0, column = 0, pady=(5,0))
        
        self.entry_ip = tk.Entry(self, width = 20, justify='center')
        self.entry_ip.grid(row = 1, column = 0)
        self.entry_ip.configure(font=('verdana', 8))
        self.entry_ip.insert(0, "192.168.0.42/8000")
        
        self.button_connect = Button(self, 2,0,1,1,"Connect")
        self.button_connect.config(command = main.connect)
        
        seperator_0 = ttk.Separator(self, orient="horizontal")
        seperator_0.grid(row = 3, column = 0, sticky = tk.E + tk.W, pady=(5,5))
        
        self.checkbutton_draw_contour = tk.Checkbutton(self, text='Draw Calibration Contour', var= main.draw_border) 
        self.checkbutton_draw_contour.grid(row=4,column = 0)
        
        self.checkbutton_detection_debug = tk.Checkbutton(self, text='Show Detection Images', var= main.debug_detection) 
        self.checkbutton_detection_debug.grid(row=5,column = 0)
        
        seperator_1 = ttk.Separator(self, orient="horizontal")
        seperator_1.grid(row = 6, column = 0, sticky = tk.E + tk.W, pady=(5,5))
        
        
        label_ip = tk.Label(self, text="Dart Detection:")
        label_ip.grid(row = 7, column = 0, pady=(0,5))
        
        label_min_pix = tk.Label(self, text="Minimum pixels for dart detection:")
        label_min_pix.grid(row = 8, column = 0)
        
        self.scale_min_pix = tk.Scale(self, from_=0, to=75000, orient=tk.HORIZONTAL, variable = main.min_pix, length = 180, sliderlength = 18)
        self.scale_min_pix.set(main.min_pix)
        self.scale_min_pix.grid(row = 9, column = 0)
        
        ### Initialize arrays for plotting ### 
        self.time_array = []
        self.pix_array = []
        self.thresh_array = []
        
        ### Initialize figure ### 
        self.fig = Figure(figsize = (2.5,2.5))
        self.ax = self.fig.add_subplot(111)
        #self.ax.set_ylim(0, 75)
        self.ax.plot(self.time_array, self.pix_array, linestyle = '-', marker = 'None', color='green', label= "Treshold")
        self.ax.plot(self.time_array, self.thresh_array, linestyle = '-', marker = 'None', color='red', label= "Pixels")
        
        self.ax.legend()
        
        self.graph = FigureCanvasTkAgg(self.fig, master= self)
        self.graph.get_tk_widget().grid(row = 7, column = 0, sticky = tk.E)
        
        seperator_2 = ttk.Separator(self, orient="horizontal")
        seperator_2.grid(row = 10, column = 0, sticky = tk.E + tk.W, pady=(5,5))
        
        label_total_count = tk.Label(self, text="Total number training images:")
        label_total_count.grid(row = 11, column = 0, pady=(5,5))
        
        self.entry_total_count = tk.Entry(self, width = 20, justify='center')
        self.entry_total_count.grid(row = 12, column = 0, pady=(5,5))
        self.entry_total_count.configure(font=('verdana', 8))
        self.entry_total_count.insert(0, "0")
        
        
    # def draw_detection_plot(self,time_array, pix_array, thresh_array):
        
    #     self.ax.plot(time_array, pix_array, linestyle = '-', marker = 'None', color='green', label= "Treshold")
    #     self.ax.plot(time_array, thresh_array, linestyle = '-', marker = 'None', color='red', label= "Pixels")
    #     self.graph.draw()
        
    

    
class Frame_UI_Video(Frame):
    
    def __init__(self, parent, width, height, row, column, main):
        
        super().__init__(parent, width, height, row, column, main)
        
        self.grid(padx = (50,0))
        
        self.canvas_video_top = Canvas(self, 502, 278, 1 ,1)
        self.canvas_video_right = Canvas(self, 502, 278, 3 ,1)
        
        label_video_top = tk.Label(self, text = "Top View")
        label_video_top.grid(row = 0, column = 1)
        
        label_video_right = tk.Label(self, text = "Side View")
        label_video_right.grid(row = 2, column = 1)
        
      

class Text_Display(tk.Text):
        
    def __init__(self, parent, width, height, row, column):
    
        super().__init__(parent)

        self.config(width = width, height = height,  relief="solid", borderwidth=1)
        self.grid(row = row, column = column, rowspan = 2, padx = (50,0), sticky= tk.W)
        

    def print_to_display(self, message):
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        statement = "\n[{0}]: {1}".format(current_time,message)
        
        self.insert(tk.END, statement)
        self.see("end")

class Canvas(tk.Canvas):

    def __init__(self, parent, width, height, row, column):
    
        super().__init__(parent)    

        self.configure(width = width, height = height, relief="solid", borderwidth=1)
        self.grid(row= row , column = column)
        
        
    def display_images(self, image, image_bl_color, image_bl_alpha, draw_border):
        
        if draw_border == 1:
                
            image = dh.add_outline_marker(image, image_bl_color, image_bl_alpha)
            self.photo = dh.resize_create(image, 40)
                    
        else:
                           
            self.photo = dh.resize_create(image, 40)
     
        self.create_image(0, 0, image = self.photo, anchor = tk.NW)


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
    
    def __init__(self, parent, width, height, row, column, main):
        
        table = tk.Frame(parent, width = 390, height = 200)  
        table.grid(row = 0, column = 0, rowspan = 4, columnspan = 4, padx = (20,0))
        table.grid_propagate(0)
        
        
        label_dart = Label(table,0,0,"Dart")
        label_X = Label(table,0,1,"X")
        label_Y = Label(table,0,2,"Y")
        label_dart1 = Label(table, 1, 0, "1")
        label_dart2 = Label(table, 2, 0,"2")
        label_dart3 = Label(table, 3, 0,"3")
        
        self.focus = 0
        
        self.list_entry_X = []
        self.list_entry_Y = []
        
        self.list_entry_X.append(Entry(table, 1, 1, main.dart_colors[0]))
        self.list_entry_X.append(Entry(table, 2, 1, main.dart_colors[1]))
        self.list_entry_X.append(Entry(table, 3, 1, main.dart_colors[2]))
        
        self.list_entry_Y.append(Entry(table, 1, 2, main.dart_colors[0]))
        self.list_entry_Y.append(Entry(table, 2, 2, main.dart_colors[1]))
        self.list_entry_Y.append(Entry(table, 3, 2, main.dart_colors[2]))
        
        
    def reset(self):
            
        #Reset table
        for entry in self.list_entry_X:
            
            entry.reset()
            
        for entry in self.list_entry_Y:
            
            entry.reset()
            
        self.focus = 0
        
        self.update_table_focus()
        
        
    def on_click(self, x, y):
        
        self.enter_value(x,y)

        if self.focus < 2:
           
           self.focus += 1
           
        self.update_table_focus()
        
        
        
    def enter_value(self, x, y):
              
        self.list_entry_X[self.focus].delete(0,20)
        self.list_entry_X[self.focus].insert(0,str(x))
            
        self.list_entry_Y[self.focus].delete(0,20)
        self.list_entry_Y[self.focus].insert(0,str(y))  
        
        
    def update_table_focus(self):
        
        # Reset all borders to default
        for entry in self.list_entry_X:
            
            entry.config(borderwidth = 1)
            
        for entry in self.list_entry_Y:
            
            entry.config(borderwidth = 1)
        
        # Apply changes to the focused ones
        self.list_entry_X[self.focus].config(borderwidth = 3)
        self.list_entry_Y[self.focus].config(borderwidth = 3) 
            
            
            
          







        
        

        
        
        
        
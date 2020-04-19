#%%
### Own imports
import dartboard
import dartshelper as dh
from DartVideoCapture import *

### Other
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.figure import Figure
import time

import tkinter as tk
import ttk as ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import numpy as np


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
            self.ax_board.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["deepskyblue"])
            self.boardCanvas.draw()
            
            ##Entry
            self.entry_dart1_X.delete(0,20)
            self.entry_dart1_X.insert(0,str(x))
            self.entry_dart1_Y.delete(0,20)
            self.entry_dart1_Y.insert(0,str(y))
              
        elif focus == 2:
            
            #Draw Cross
            self.ax_board.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["orangered"])
            self.boardCanvas.draw()
            
            self.entry_dart2_X.delete(0,20)
            self.entry_dart2_X.insert(0,str(x))
            self.entry_dart2_Y.delete(0,20)
            self.entry_dart2_Y.insert(0,str(y))
            
        elif focus == 3:
            
            #Draw Cross
            self.ax_board.plot(x, y, "+", markersize = 18, mew = 3.5, c = self.colors["darkmagenta"])
            self.boardCanvas.draw()
            
            
            self.entry_dart3_X.delete(0,20)
            self.entry_dart3_X.insert(0,str(x))
            self.entry_dart3_Y.delete(0,20)
            self.entry_dart3_Y.insert(0,str(y))
        
        
        
    
    def on_click(self,event):
        
        if event.inaxes is not None:
            
            
            self.enter_value_focus(round(event.xdata,3),round(event.ydata,3), self.dart_count_table)
            
            self.dart_count_table = self.dart_count_table + 1
            
            self.set_table_focus(self.dart_count_table)
        
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

            self.dart_count_table = 1
            self.set_table_focus(self.dart_count_table)
            
            #Reset darboard
            self.boardCanvas.get_tk_widget().grid_remove()
            self.create_board_canvas()
            
            self.print_to_display("Values resetted!")
            
            
    def print_to_display(self,message):
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        
        statement = "\n[{0}]: {1}".format(current_time,message)
        
        self.text_display.insert(tk.END, statement)
        self.text_display.see("end")
    
    def connect(self):
        
        url = "http://192.168.0.42:8000/video_feed"
        
        try:
            self.print_to_display("Trying to connect...")
            self.vid = DartsVideoCapture(url)
            self.connected = True
            self.print_to_display("Sucessfully connected!")
            self.time_start_throw = time.time()
        except:
            
            self.print_to_display("Could not connect - Please check raspberry pi!")
            
            
    def display_images(self, t_image_raw, r_image_raw):
        
        if self.draw_border.get() == 1:
                    
            t_image = dh.add_outline_marker(t_image_raw, self.t_bl_color, self.t_bl_alpha)
            r_image = dh.add_outline_marker(r_image_raw, self.r_bl_color, self.r_bl_alpha)
                    
            self.photoTop = dh.resize_create(t_image, 40)
            self.photoRight = dh.resize_create(r_image, 40)
                    
        else:
                    
                    
            self.photoTop = dh.resize_create(t_image_raw, 40)
            self.photoRight = dh.resize_create(r_image_raw, 40)
             
        self.canvas_video_top.create_image(0, 0, image = self.photoTop, anchor = tk.NW)
        self.canvas_video_right.create_image(0, 0, image = self.photoRight, anchor = tk.NW)
        
        
    def detect_darts(self, t_image, r_image, t_image_raw, r_image_raw):
        
        if self.detection:
            
                time_since_last_throw = round(time.time() - self.time_last_throw, 2)
                
                ## Get pixel differences over the two pictures
                t_dif_pix, self.t_firstFrame = dh.calc_background_dif(t_image, self.t_firstFrame, "TOP", False)
                
                r_dif_pix, self.r_firstFrame = dh.calc_background_dif(r_image, self.r_firstFrame, "RIGHT", False)
                
                dif_pix = t_dif_pix + r_dif_pix
                
                
                min_pix = self.scale_min_pix.get()
                
                ##Draw
                self.draw_detection_plot()

                if dif_pix > min_pix and time_since_last_throw > 0.5:
                
                    self.time_last_throw = time.time()
                    
                    
                    #Set the Background frames to None to force the app to get new images after the delay
                    self.t_firstFrame = None
                    self.r_firstFrame = None
                    
                    self.dart_counter = self.dart_counter + 1    
                    
                    
                    self.print_to_display(str(self.dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
                    
                    
                    if self.dart_counter == 1:
                        
                        self.t_dart_images.append(t_image_raw)
                        self.r_dart_images.append(r_image_raw)
                    
                    elif self.dart_counter == 2:
                        
                        self.t_dart_images.append(t_image_raw)
                        self.r_dart_images.append(r_image_raw)
                    
                    
                    elif self.dart_counter == 3:
                        
                        self.t_dart_images.append(t_image_raw)
                        self.r_dart_images.append(r_image_raw)
                        
                        
                        self.detection = False
                        self.print_to_display("Detection set to False, get the darts")
                        
                        self.time_start_throw = time.time()
                        self.button_save_and_next.config(state = "normal")
                        
                  ##Working
                        
                    ##Delay a bit to get a still board again
                    time.sleep(self.delay_after_shot)
                
                # Save Data for analysis
                self.pix_array.append(dif_pix/1000)
                self.thresh_array.append(min_pix/1000)
                self.time_array.append(round(time.time() - self.time_start_throw,2))
    
    def draw_detection_plot(self):
        
        self.ax.plot(self.time_array, self.pix_array, linestyle = '-', marker = 'None', color='green', label= "Treshold")
        self.ax.plot(self.time_array, self.thresh_array, linestyle = '-', marker = 'None', color='red', label= "Pixels")
        self.graph.draw()
        
    def next_throw(self):
        
        self.ax.cla()
        self.detection = True
        self.dart_count_detection = 0
        self.time_start_throw = time.time()
   
   
    def update(self):
        
        if self.connected == True:
        
            # Get a frame from the video source
            ret, frame = self.vid.get_frame()
        
            if ret:
            
                t_image, r_image, t_image_raw, r_image_raw = dh.process_frame(frame, 31)
                
                self.display_images(t_image_raw, r_image_raw)
                
                self.detect_darts(t_image, r_image, t_image_raw, r_image_raw)
                
                
                

        self.window.after(self.delay, self.update)
        
        
            
###-------------GUI-Creation--------------- 
# Frames and widgets are created from top to bottom and from left to right!


    def create_board_canvas(self):
        
        self.fig_board, self.ax_board = dartboard.Draw_Dartboard()
        mng = plt.get_current_fig_manager()
        mng.window.showMinimized()
        self.boardCanvas = FigureCanvasTkAgg(self.fig_board, master= self.window)
        
        plt.close('all')
       
        self.boardCanvas.get_tk_widget().config(width = 640, height = 640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=0, column=0, rowspan = 3)
        
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
    def create_UI_frame_left(self):
        
        ## UI
        self.UIFrame_left = tk.Frame(self.window, width = 640, height = 100)
        #self.UIFrame_left.grid_propagate(0)
        self.UIFrame_left.grid(row=3, column=0, rowspan = 2)

        self.create_table()
        
        self.button_reset = self.create_button(self.UIFrame_left,0, 5, 1, 1, "Reset Values")
        self.button_reset.config(command = self.reset, bg = "red",width = 12, height = 2)
        
        self.button_cancel = self.create_button(self.UIFrame_left,0, 6, 1, 1, "Cancel Throwing")
        self.button_cancel.config(bg = "red",width = 12, height = 2)
        
        self.button_delete_and_next = self.create_button(self.UIFrame_left,1, 5, 2, 1, "Delete & \n Next Throw")
        self.button_delete_and_next.config(bg = "red",width = 12, height = 6, state = "disabled")
        
        self.button_save_and_next = self.create_button(self.UIFrame_left,1, 6, 2, 1, "Save & \n Next Throw")
        self.button_save_and_next.config(command = self.next_throw, bg = "green", width = 12, height = 6, state = "disabled")
        
    
    def create_video_frame(self):
        
        ## Video
        videoFrame = tk.Frame(self.window, width = 532, height = 640 )
        videoFrame.grid(row=0, column=2, rowspan = 2, padx = (50,0), sticky= tk.NW)
        videoFrame.grid_propagate(0)
        
        self.canvas_video_top = tk.Canvas(videoFrame, width = 502, height = 278, relief="solid", borderwidth=1)
        self.canvas_video_top.grid(row=1,column = 1)

        self.canvas_video_right = tk.Canvas(videoFrame, width = 502, height = 278, relief="solid", borderwidth=1)
        self.canvas_video_right.grid(row=3,column = 1)
        
        
        label_video_top = tk.Label(videoFrame, text = "Top View")
        label_video_top.grid(row = 0, column = 1)
        
        label_video_right = tk.Label(videoFrame, text = "Side View")
        label_video_right.grid(row = 2, column = 1)
        
        
    def create_UI_frame_right(self):
       
        UIFrame = tk.Frame(self.window,relief="solid", borderwidth=1)
        #UIFrame.grid_propagate(0)
        UIFrame.grid(row=0, column=1, sticky = tk.N)
        
        label_ip = tk.Label(UIFrame, text="Video Address:")
        label_ip.grid(row = 0, column = 0, pady=(5,0))
        
        self.entry_ip = tk.Entry(UIFrame, width = 20, justify='center')
        self.entry_ip.grid(row = 1, column = 0)
        self.entry_ip.configure(font=('verdana', 8))
        self.entry_ip.insert(0, "192.168.0.42/8000")
        
        self.button_connect = self.create_button(UIFrame,2,1,1,1, "Connect")
        self.button_connect.config(command = self.connect)
        self.button_connect.grid(row = 2, column = 0)
        
        seperator_0 = ttk.Separator(UIFrame, orient="horizontal")
        seperator_0.grid(row = 3, column = 0, sticky = tk.E + tk.W, pady=(5,5))
        
        self.checkbutton_draw_contour = tk.Checkbutton(UIFrame, text='Draw Calibration Contour', var= self.draw_border) 
        self.checkbutton_draw_contour.grid(row=4,column = 0)
        
        seperator_0 = ttk.Separator(UIFrame, orient="horizontal")
        seperator_0.grid(row = 5, column = 0, sticky = tk.E + tk.W, pady=(5,5))
        
        
        label_ip = tk.Label(UIFrame, text="Dart Detection:")
        label_ip.grid(row = 6, column = 0, pady=(0,5))
        
        label_min_pix = tk.Label(UIFrame, text="Minimum pixels for dart detection:")
        label_min_pix.grid(row = 8, column = 0)
        
        self.scale_min_pix = tk.Scale(UIFrame, from_=0, to=75000, orient=tk.HORIZONTAL, variable = self.min_pix, length = 180, sliderlength = 18)
        self.scale_min_pix.set(self.min_pix)
        self.scale_min_pix.grid(row = 9, column = 0)
        
        self.fig = Figure(figsize = (2.5,2.5))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0, 75)
        self.ax.plot(self.time_array, self.pix_array, linestyle = '-', marker = 'None', color='green', label= "Treshold")
        self.ax.plot(self.time_array, self.thresh_array, linestyle = '-', marker = 'None', color='red', label= "Pixels")
        
        self.ax.legend()
        
        self.graph = FigureCanvasTkAgg(self.fig, master= UIFrame)
        self.graph.get_tk_widget().grid(row = 7, column = 0, sticky = tk.E)
        
        
        
    def create_display_frame(self):
        
        self.text_display = tk.Text(self.window, height= 10, width = 65, relief="solid", borderwidth=1)
        self.text_display.grid(row=3, column=2, rowspan = 2, padx = (50,0), sticky= tk.W)
        
         
    def create_button(self, parent, row, column,rowspan, columnspan, text):
        button = tk.Button(parent, text = text)
        button.grid(row=row, column = column, rowspan = rowspan, columnspan = columnspan, padx=(5, 5), pady=(5,5))
        button.config(font=('verdana', 10))
        
        return button
        
        
    def create_table(self):
        
        ## Table
        table = tk.Frame(self.UIFrame_left, width = 390, height = 200)  
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
    
    
    def __init__(self, window, window_title):
    

        # Darts Detection
        self.detection = True
        self.min_pix = 25000
        self.dart_counter = 0
        self.time_last_throw = time.time() - 1
        self.t_firstFrame = None
        self.r_firstFrame = None
        self.delay_after_shot = 1
        self.dart_count_detection = 0
        
        # Threshold
        self.pix_array = []
        self.time_array = []
        self.thresh_array = []
        
        # Results
        self.t_dart_images = []
        self.r_dart_images = []
        
        self.dart_count_table = 1
        
        ##Timings
        
        
        
        ## ---- UI ---- ##
        
        ## Variables
        self.colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        self.connected = False
        self.draw_border = tk.IntVar()
        
        
        self.window = window
        self.window.geometry("1900x840")    
        self.window.resizable(0, 0)
        self.window.title(window_title)
    
        self.create_board_canvas()
        
        self.create_UI_frame_left()
        
        self.create_display_frame()
        
        self.create_video_frame()
        
        self.create_UI_frame_right()
        
        self.set_table_focus(self.dart_count_table)
        
        
        ## Create baseline images
        t_bl = cv2.imread("t_image_raw_baseline.jpg")
        r_bl = cv2.imread("r_image_raw_baseline.jpg")
        
        self.t_bl_color, self.t_bl_alpha = dh.outline_from_image(t_bl, 180, 300, 500)
        self.r_bl_color, self.r_bl_alpha = dh.outline_from_image(r_bl, 180, 300, 500)
        
        
 
        
        self.print_to_display("Application started...")
        self.print_to_display("Waiting for video device...")
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        
        
        
                
        self.window.mainloop()


if __name__ == "__main__":
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP")
    
    



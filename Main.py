import BoardCanvas

from DartsVideoCapture import DartsVideoCapture

import dartshelper as dh
import darts_UI
from Dart_Detector import Dart_Detector
from CSV_Handler import CSV_Handler

import tkinter as tk
import time
import cv2
import csv

from matplotlib import colors as mcolors

from pathlib import Path


class Main:
    
    def start(self):
        
        self.text_display.print_to_display("Application started...")
        self.time_last_throw = time.time()
        self.frame_UI_left.table.update_table_focus()
        
        self.csv_handler.count_lines()
        
        
    def reset(self):
        
        self.frame_UI_left.table.reset()
        self.canvas_board.reset()
    
    def next_throw(self):
        
        ### Save
        self.save()
        
        ### Reset
        self.reset()
        self.dart_detector.reset()
        self.dart_detector.detection = True
        self.dart_count = 0
        
    def connect(self):
        
        self.url = "http://192.168.0.42:8000/video_feed"
        
        self.text_display.print_to_display("Connecting to " + self.url)
        
        try:
            
            self.vid = DartsVideoCapture(self.url)
            self.connected = True
            self.text_display.print_to_display("Sucessfully connected!")
            self.time_start_throw = time.time()
            
        except:
            
            self.text_display.print_to_display("Could not connect - Please check raspberry pi!")
            
            
    def save(self):
        
        count = 0
        
        for darts in self.dart_detector.image_result:
            
            x = self.frame_UI_left.table.list_entry_X[count].get()
            y = self.frame_UI_left.table.list_entry_Y[count].get()
            
            
            disp_name = str(count) + " X: " + x + " Y: " + y

            x_file = str(x).replace(".","")
            y_file = str(y).replace(".","")

            ## Save Image

            temp_name = "/total_count_" +  str(count) + "_" + x_file + "_" + y_file + ".jpg"

            file_name = str(self.dir) + temp_name
            
            cv2.imshow(disp_name, self.dart_detector.image_result[count])
                        
            cv2.imwrite(file_name, self.dart_detector.image_result[count])
            
            ## Save csv
            
            self.csv_handler.save_result(count, x, y)
            
            count += 1
            
        self.csv_handler.count_lines()
        
           
    def update(self):
        
        if self.connected == True:
        
            # Get a frame from the video source
            ret, frame = self.vid.get_frame()
        
            if ret:
            
                self.image_top, self.image_right, self.image_raw_top, self.image_raw_right = dh.process_frame(frame, 31)
                
                #### UMSCHREIBEN DER VARIABLEN NAMEN IN RICHTIGE REIHENFOLGE ####
                self.frame_UI_video.canvas_video_top.display_images(self.image_raw_top, self.t_bl_color, self.t_bl_alpha, self.draw_border.get())
                self.frame_UI_video.canvas_video_right.display_images(self.image_raw_right, self.r_bl_color, self.r_bl_alpha, self.draw_border.get())
                
                self.dart_detector.detect()
                self.dart_detector.draw_detection_plot()

        self.window.after(self.delay, self.update)
    
        
    def __init__(self, window):

        self.window = window
        self.window.geometry("1500x840")    
        self.window.resizable(0, 0)
        self.window.title("DartyP")      
        
        ### Static changeables
        
        self.url = "http://192.168.0.42:8000/video_feed"
        
        self.dir = Path('F:/Darts_Results/')
        
        
        ### Initilialize variables ###
        self.delay = 1
        self.connected = False
        self.detection = True
        self.draw_border = tk.IntVar()
        self.debug_detection = tk.IntVar()
        self.min_pix = 25000
        self.first_frame_top = None
        self.first_frame_right = None
        self.first_frame_top_raw = None
        self.first_frame_right_raw = None
        self.dart_count = 0
       
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        dart_colors = []
        dart_colors.append(colors["deepskyblue"])
        dart_colors.append(colors["orangered"])
        dart_colors.append(colors["darkmagenta"])
        
        self.dart_colors = dart_colors
        
        # Results
        self.t_dart_images = []
        self.r_dart_images = []
        
        ### Create Baseline images from data ###
        self.t_bl_color, self.t_bl_alpha = dh.outline_from_image(cv2.imread("t_image_raw_baseline.jpg"), 180, 300, 500)
        self.r_bl_color, self.r_bl_alpha = dh.outline_from_image(cv2.imread("r_image_raw_baseline.jpg"), 180, 300, 500)
        

        self.canvas_board = BoardCanvas.BoardCanvas(self.window, 640, 640, 0, 0, self)
        
        self.frame_UI_left = darts_UI.Frame_UI_Left(self.window, 640, 300, 3, 0, self)       
        
        self.frame_UI_right = darts_UI.Frame_UI_Right(self.window, 0, 0, 0, 1, self)
        
        self.frame_UI_video = darts_UI.Frame_UI_Video(self.window, 532, 640, 0, 2, self)
        
        self.text_display = darts_UI.Text_Display(self.window, 65, 10, 3, 2)
        
        self.dart_detector = Dart_Detector(self)
        
        self.csv_handler = CSV_Handler(self)
        
        self.start()
        
        self.update()
        
        self.window.mainloop()
                
        
if __name__ == "__main__":
    
    root = tk.Tk()
    GUI = Main(root)
    
import BoardCanvas

from DartsVideoCapture import DartsVideoCapture

import dartshelper as dh
import darts_UI

import tkinter as tk
import time
import cv2

from matplotlib import colors as mcolors


class Main:
    
    def start(self):
        
        self.text_display.print_to_display("Application started...")
        self.time_last_throw = time.time()
        self.frame_UI_left.table.update_table_focus()
    
    def reset(self):
        
        self.frame_UI_left.table.reset()
        self.canvas_board.reset()
    
    def next_throw(self):
        
        print("next_throw_dummy_action")
    
    def connect(self):
        
        url = "http://192.168.0.42:8000/video_feed"
        
        self.text_display.print_to_display("Connecting to " + url)
        
        try:
            
            self.vid = DartsVideoCapture(url)
            self.connected = True
            self.text_display.print_to_display("Sucessfully connected!")
            self.time_start_throw = time.time()
            
        except:
            
            self.text_display.print_to_display("Could not connect - Please check raspberry pi!")
            
            
    def update(self):
        
        if self.connected == True:
        
            # Get a frame from the video source
            ret, frame = self.vid.get_frame()
        
            if ret:
            
                t_image, r_image, t_image_raw, r_image_raw = dh.process_frame(frame, 31)
                
                self.frame_UI_video.canvas_video_top.display_images(t_image_raw, self.t_bl_color, self.t_bl_alpha, self.draw_border.get())
                self.frame_UI_video.canvas_video_right.display_images(r_image_raw, self.r_bl_color, self.r_bl_alpha, self.draw_border.get())
                
                pix_dif_top, self.t_first_frame = dh.detect_darts(self.detection, self.time_last_throw, t_image, self.t_first_frame)
                pix_dif_right, self.r_first_frame,  = dh.detect_darts(self.detection, self.time_last_throw, r_image, self.r_first_frame)
                pix_dif = pix_dif_top + pix_dif_right
                
                
                min_pix = self.frame_UI_right.scale_min_pix.get()
                
                time_since_last_throw = round(time.time() - self.time_last_throw, 2)


                if pix_dif > min_pix and time_since_last_throw > 0.5:
                    
                    
                    self.dart_count_detection = dh.count_and_save(self, self.dart_count_detection, t_image_raw, r_image_raw, pix_dif)
         

        self.window.after(self.delay, self.update)
    
        
    def __init__(self, window):

        self.window = window
        self.window.geometry("1900x840")    
        self.window.resizable(0, 0)
        self.window.title("DartyP")      
        
        ### Initilialize variables ###
        self.delay = 1
        self.connected = False
        self.detection = True
        self.draw_border = tk.IntVar()
        self.min_pix = 30000
        self.t_first_frame = None
        self.r_first_frame = None
        self.dart_count_detection = 0
        self.dart_count_table = 1

        
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
        
        self.start()
        
        self.update()
        
        self.window.mainloop()
                
        
if __name__ == "__main__":
    
    root = tk.Tk()
    GUI = Main(root)
    
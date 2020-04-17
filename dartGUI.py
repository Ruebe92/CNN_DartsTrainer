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
            
        else:

            print ('Clicked ouside axes bounds but inside plot window')
       
    
    def __init__(self, window, window_title, video_source):
    
        window.resizable(0, 0)
        
        fig, ax = dartboard.Draw_Dartboard()
        
    def create_root():
        
        
        self.boardCanvas = FigureCanvasTkAgg(fig, master= window)
        self.boardCanvas.get_tk_widget().config(width=640, height=640, cursor="target")
        self.boardCanvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=2)
        self.boardCanvas.draw()
        self.boardCanvas.mpl_connect('button_press_event', self.on_click)
        
        self.videoCanvasTop = tk.Canvas(window, width = 320, height = 180)
        self.videoCanvasTop.grid(row=0,column=0)
        self.videoCanvasRight = tk.Canvas(window,width= 320, height= 180)
        self.videoCanvasRight.grid(row=0,column=1)
        
        self.dart1CanvasTop = tk.Canvas(window,width=320, height=180)
        self.dart1CanvasTop.grid(row=0,column=2)
        self.dart2CanvasTop = tk.Canvas(window,width=320, height=180)
        self.dart2CanvasTop.grid(row=1,column=2)
        self.dart3CanvasTop = tk.Canvas(window,width=320, height=180)
        self.dart3CanvasTop.grid(row=2,column=2)
        
        
        self.dart1CanvasRight = tk.Canvas(window,width=320, height=180)
        self.dart1CanvasRight.grid(row=0,column=3) 
        self.dart2CanvasRight = tk.Canvas(window,width=320, height=180)
        self.dart2CanvasRight.grid(row=1,column=3)
        self.dart3CanvasRight = tk.Canvas(window,width=320, height=180)
        self.dart3CanvasRight.grid(row=2,column=3)
        
        self.UIFrame = tk.Frame(window)
        self.UIFrame.grid(row=3, column=0, columnspan=4, rowspan=2)
        
        self.table = tk.Frame(self.UIFrame)
        self.table.grid(row=0, column=0, columnspan=3, rowspan=3)
        
        tk.Label(self.table, text = "Dart").grid(row=0, column=0)
        tk.Label(self.table, text = "X").grid(row=0, column=1)
        tk.Label(self.table, text = "Y").grid(row=0, column=2)
        tk.Label(self.table, text = "1").grid(row=1, column=0)
        tk.Label(self.table, text = "2").grid(row=2, column=0)
        tk.Label(self.table, text = "3").grid(row=3, column=0)
        
        
        self.d1_X = tk.Entry(self.table, text="")
        self.d1_X.grid(row=1, column=1)
        
        self.d1_Y = tk.Entry(self.table, text="")
        self.d1_Y.grid(row=1, column=2)
        
        self.d2_X = tk.Entry(self.table, text="")
        self.d2_X.grid(row=2, column=1)
        
        self.d2_Y = tk.Entry(self.table, text="")
        self.d2_Y.grid(row=2, column=2)
        
        self.d3_X = tk.Entry(self.table, text="")
        self.d3_X.grid(row=3, column=1)
        
        self.d3_Y = tk.Entry(self.table, text="")
        self.d3_Y.grid(row=3, column=2)
        
        
        self.pb_NextThrow = tk.Button(self.UIFrame, text = 'Next Throw', command = self.next_Throw, width = 20)
        self.pb_NextThrow.grid(row = 0 , column = 4, pady = '10')
       

        self.pb_Delete = tk.Button(self.UIFrame, text = 'Delete Table', width=20)
        self.pb_Delete.grid(row = 1, column = 4, pady = '10')
        
        self.entry_Console = tk.Entry(self.UIFrame, text = '.........', width= 40)
        self.entry_Console.grid(row = 2, column=4, columnspan=2, pady = '10')
        self.entry_Console.insert(0,"Waiting for user...")
       
        plt.close('all')
        
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        # open video source (by default this will try to open the computer webcam)        
        self.vid = MyVideoCapture(self.video_source)
         
        # Darts Detection
        self.detection = True
        self.min_pix = 15000
        self.dart_counter = 0
        self.time_last_throw = time_start - 1
        self.t_firstFrame = None
        self.r_firstFrame = None
        
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        
        self.window.mainloop()
    
    def next_Throw(self):
        
        self.detection = True
        self.dart_counter = 0
        self.entry_Console.delete(0,40)
        self.entry_Console.insert(0,"Waiting for user...")    
        self.dart1CanvasTop.delete("all")
        self.dart2CanvasTop.delete("all")
        self.dart3CanvasTop.delete("all")
        self.dart1CanvasRight.delete("all")
        self.dart2CanvasRight.delete("all")
        self.dart3CanvasRight.delete("all")
        
      
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            
            t_image, r_image, t_image_raw, r_image_raw = dh.process_frame(frame, 31)
            
            
            ## Dart detection
            if self.detection:
            
                time_since_last_throw = round(time.time() - self.time_last_throw, 2)
                
                ## Get pixel differences over the two pictures
                t_dif_pix, self.t_firstFrame = dh.calc_background_dif(t_image, self.t_firstFrame, "TOP", False)
                
                r_dif_pix, self.r_firstFrame = dh.calc_background_dif(r_image, self.r_firstFrame, "RIGHT", False)
                
                dif_pix = t_dif_pix + r_dif_pix
                
                if dif_pix > self.min_pix and time_since_last_throw > 0.5:
                
                    self.time_last_throw = time.time()
                    
                    
                    
                    dart_array.append(10000)
                    
                    
                    #Set the Background frames to None to force the app to get new images after the delay
                    self.t_firstFrame = None
                    self.r_firstFrame = None
                    
                    time.sleep(delay_after_shot)
                
                    self.dart_counter = self.dart_counter + 1    
                    
                   
                    
                    self.entry_Console.delete(0,40)
                    self.entry_Console.insert(0, str(self.dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
                    print(str(self.dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
                    
                    
                    if self.dart_counter == 1:
                        
                        self.t_photo1 = dh.resize_create(t_image_raw, 25)
                        self.dart1CanvasTop.create_image(0, 0, image = self.t_photo1, anchor = tk.NW)
                        
                        self.r_photo1 = dh.resize_create(r_image_raw, 25)
                        self.dart1CanvasRight.create_image(0, 0, image = self.r_photo1, anchor = tk.NW)
                        
                        t_dart_images.append(t_image_raw)
                        r_dart_images.append(r_image_raw)
                    
                    elif self.dart_counter == 2:
                        
                        self.t_photo2 = dh.resize_create(t_image_raw, 25)
                        self.dart2CanvasTop.create_image(0, 0, image = self.t_photo2, anchor = tk.NW)
                        
                        self.r_photo2 = dh.resize_create(r_image_raw, 25)
                        self.dart2CanvasRight.create_image(0, 0, image = self.r_photo2, anchor = tk.NW)
                        
                        t_dart_images.append(t_image_raw)
                        r_dart_images.append(r_image_raw)
                    
                    
                    elif self.dart_counter == 3:
                        
                        self.t_photo3 = dh.resize_create(t_image_raw, 25)
                        self.dart3CanvasTop.create_image(0, 0, image = self.t_photo3, anchor = tk.NW)
                        
                        self.r_photo3 = dh.resize_create(r_image_raw, 25)
                        self.dart3CanvasRight.create_image(0, 0, image = self.r_photo3, anchor = tk.NW)
                        
                        t_dart_images.append(t_image_raw)
                        r_dart_images.append(r_image_raw)
                        
                        
                        self.detection = False
                        self.entry_Console.delete(0,40)
                        self.entry_Console.insert(0, "Detection set to False, get the darts")
                        
                        print(str(self.dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
                        
                        
                    
                else: 
                    
                    dart_array.append(0)
                
                
                # Save Data for analysis
                t_pix_array.append(t_dif_pix)
                r_pix_array.append(r_dif_pix)
                pix_array.append(dif_pix)
                time_array.append(round(time.time() - time_start,2))
           
            ##Displaying Videos
            
            self.photoTop = dh.resize_create(t_image_raw, 25)
            self.photoRight = dh.resize_create(r_image_raw, 25)
                        
            self.videoCanvasTop.create_image(0, 0, image = self.photoTop, anchor = tk.NW)
            self.videoCanvasRight.create_image(0, 0, image = self.photoRight, anchor = tk.NW)
     
        self.window.after(self.delay, self.update) 
        

        
             

class MyVideoCapture:
     
    def __init__(self, video_source):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height         
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR                 
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))             
             else:
                 return (ret, None)
         else:
             return (ret, None) 
     
    # Release the video source when the object is destroyed
    def __del__(self):         
        
        if self.vid.isOpened():             

            self.vid.release()    



if __name__ == "__main__":
    
    #%% Dart Detection
    
    draw = False
    delay_after_shot = 0.5

    t_dart_images = []
    r_dart_images = []

    t_baseline_Frame = None
    r_baseline_firstFrame = None
    
    
    
    dart_images = []
    
    #UI
    text = "No Dart"
    
    
    # Timings
    time_start = time.time()
    
    
    pix_array = []
    time_array = []
    t_pix_array = []
    r_pix_array = []
    dart_array = []
    
    
    url = "http://192.168.0.42:8000/video_feed"
    
    root = tk.Tk()
    
    GUI = dartsGUI(root, "DartyP", url)
    
    



#%%
### Own imports
import dartboard
import imageProcesses as iP

### Other
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import cv2


def on_click(event):
    if event.inaxes is not None:
        
        print (round(event.xdata,2), round(event.ydata,2))
    else:
        
        print ('Clicked ouside axes bounds but inside plot window')
        
        
    

class dartsGUI:  
    
    def __init__(self, window, window_title, video_source):
    
        root.resizable(0, 0)
    
        fig, ax = dartboard.Draw_Dartboard()
        
        self.videoCanvasTop = tk.Canvas(root, width = 320, height = 180, bg = "white")
        self.videoCanvasTop.grid(row=0,column=0)
        self.videoCanvasRight = tk.Canvas(root,width= 320, height= 180, bg = "white")
        self.videoCanvasRight.grid(row=0,column=1)
        
        self.dart1CanvasTop = tk.Canvas(root,width=320, height=180, bg = "grey")
        self.dart1CanvasTop.grid(row=0,column=2)
        self.dart2CanvasTop = tk.Canvas(root,width=320, height=180, bg = "grey")
        self.dart2CanvasTop.grid(row=1,column=2)
        self.dart3CanvasTop = tk.Canvas(root,width=320, height=180, bg = "grey")
        self.dart3CanvasTop.grid(row=2,column=2)
        
        
        self.dart1CanvasRight = tk.Canvas(root,width=320, height=180, bg = "green")
        self.dart1CanvasRight.grid(row=0,column=3) 
        self.dart2CanvasRight = tk.Canvas(root,width=320, height=180, bg = "green")
        self.dart2CanvasRight.grid(row=1,column=3)
        self.dart3CanvasRight = tk.Canvas(root,width=320, height=180, bg = "green")
        self.dart3CanvasRight.grid(row=2,column=3)
        
        
        
        self.boardCanvas = FigureCanvasTkAgg(fig, master=root)
        self.boardCanvas.get_tk_widget().config(width=640, height=640)
        self.boardCanvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=2)
        self.boardCanvas.draw()
        self.boardCanvas.mpl_connect('button_press_event',on_click)
        
        self.UIFrame = tk.Frame(root)
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
        
        
        self.pb_NextThrow = tk.Button(self.UIFrame, text = 'Next Throw', width=20)
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
         
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        
        self.window.mainloop()
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        
        if ret:
            
            t_image, r_image, t_image_raw, r_image_raw = iP.process_frame(frame, 31)
            
            scale_percent = 25 # percent of original size
            width = int(t_image.shape[1] * scale_percent / 100)
            height = int(t_image.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image 
            resizedTop = cv2.resize(t_image_raw, dim, interpolation = cv2.INTER_AREA) 
            
            resizedRight = cv2.resize(r_image_raw, dim, interpolation = cv2.INTER_AREA) 
            
            
            
            self.photoTop = ImageTk.PhotoImage(image = Image.fromarray(resizedTop))
            self.videoCanvasTop.create_image(0, 0, image = self.photoTop, anchor = tk.NW)
            
            self.photoRight = ImageTk.PhotoImage(image = Image.fromarray(resizedRight))
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
    
    url = "http://192.168.0.42:8000/video_feed"
    
    root = tk.Tk()
    GUI = dartsGUI(root, "DartyP", url)
    
    root.mainloop()


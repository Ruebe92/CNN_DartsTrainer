import imageio
import imutils
import numpy as np
import cv2
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as pat

import tkinter as tk
from PIL import ImageTk, Image

import imageProcesses as iP
import dartGUI as dartGUI




class App:

    def __init__(self, window, window_title, video_source):
        
        self.window = dartGUI.dartsGUI()
        self.window.title(window_title)
        self.video_source = video_source
    
        # open video source (by default this will try to open the computer webcam)        
        #self.vid = MyVideoCapture(self.video_source)
    
        # Create a canvas that can fit the above video source size
        #self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        #self.canvas.pack()
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        #self.update()
    
        self.window.mainloop()
 
 
    # def update(self):
    #     # Get a frame from the video source
    #     ret, frame = self.vid.get_frame()
    
    #     if ret:
    #         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    #         self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
     
    #     self.window.after(self.delay, self.update)  
 

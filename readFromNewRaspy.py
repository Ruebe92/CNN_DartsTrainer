import imutils
import numpy as np
import cv2
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as pat

#%% Video Stream

url = "http://192.168.0.42:8000/video_feed"
cap = cv2.VideoCapture(url)


#%% Dart Detection

t_baseline_Frame = None
r_baseline_firstFrame = None

min_area = 400      #Minimal contour size to detect a valid dart

dart_counter = 0
dart_images = []

#UI
text = "No Dart"


# Timings
time_start = time.time()
time_last_throw = time_start - 1

pix_array = []
time_array = []
t_pix_array = []
r_pix_array = []
dart_array = []


#%% Functions

def process_frame(frame, blur):
    
    
    image_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      #Grayscale
    image_processed = cv2.GaussianBlur(image_processed, (51, 51), 0)         #Blur
        
    t_image_processed = image_processed[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_processed = image_processed[int(image_processed.shape[0]/2) + 1 :,:]
    
    t_image_raw = frame[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_raw = frame[int(image_processed.shape[0]/2) + 1 :,:] 
    
    return t_image_processed, r_image_processed, t_image_raw, r_image_raw


def calc_background_dif(image, background_image, name):
    
    if background_image is None:
        
        background_image = image
    
    frameDelta = cv2.absdiff(background_image, image)
    
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(cnts)
	
    debug_image = cv2.cvtColor(frameDelta,cv2.COLOR_GRAY2RGB)
    
    n_dif_pix = []
    
    if len(contours) != 0:
        
        # draw in blue the contours that were found
        cv2.drawContours(debug_image, contours, -1, 255, 3)
        
        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        
        # draw the biggest contour (c) in green
        cv2.rectangle(debug_image,(x,y),(x+w,y+h),(0,255,0),2)
    
    
        for con in contours: 
            
            
            if cv2.contourArea(con) > 400:
                
                print(name + "  " +str(cv2.contourArea(con)))
                
                n_dif_pix.append(cv2.contourArea(con))
                
                            
        n_dif_pix_tot = sum(n_dif_pix)
    
    else:
        
        n_dif_pix_tot = 0
    
    

    cv2.imshow(name, debug_image)
    
    return n_dif_pix_tot, background_image
    
    

#%% Main-Loop

draw = False

t_firstFrame = None
r_firstFrame = None
delay_after_shot = 0.25

t_dart_images = []
r_dart_images = []

while(cap.isOpened()):
    
    ret, frame = cap.read()    
    
    if ret == True:
        
        time_since_last_throw = round(time.time() - time_last_throw, 2)
        
        
        t_image, r_image, t_image_raw, r_image_raw = process_frame(frame, 30)
        
        
        t_dif_pix, t_firstFrame = calc_background_dif(t_image, t_firstFrame, "TOP")
        
        r_dif_pix, r_firstFrame = calc_background_dif(r_image, r_firstFrame, "RIGHT")
        
        dif_pix = t_dif_pix + r_dif_pix
        
        
        if dif_pix > 30000 and time_since_last_throw > 0.66:
        
            time_last_throw = time.time()
            
            
            
            dart_array.append(10000)
            
            
            #Set the Background frames to None to force the app to get new images after the delay
            t_firstFrame = None
            r_firstFrame = None
            
            time.sleep(delay_after_shot)
        
            dart_counter = dart_counter + 1    
            
            t_dart_images.append(t_image_raw)
            r_dart_images.append(r_image_raw)
            
            print(str(dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
        
        else: 
            
            dart_array.append(0)
        
        
        # Save Data for analysis
        t_pix_array.append(t_dif_pix)
        r_pix_array.append(r_dif_pix)
        pix_array.append(dif_pix)
        
        time_array.append(round(time.time() - time_start,2))
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if dart_counter == 3:
        break
        
    
cap.release()
cv2.destroyAllWindows()
plt.close('all')

#%%


fig, axes = plt.subplots(nrows = 3, ncols = 2, figsize = (10,10))
      
axes[0][0].imshow(t_dart_images[0])
axes[0][1].imshow(r_dart_images[0])

axes[1][0].imshow(t_dart_images[1])
axes[1][1].imshow(r_dart_images[1])      

axes[2][0].imshow(t_dart_images[2])
axes[2][1].imshow(r_dart_images[2]) 
            
 

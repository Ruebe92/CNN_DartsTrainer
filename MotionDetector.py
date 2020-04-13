# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.patches as pat

#%%

capture = cv2.VideoCapture('http://pi:raspberry@192.168.0.40:8081')

firstFrame = None
min_area = 400  #Minimal contour size to detect a valid dart
dart_counter = 0
time_last_throw = time.time() - 1

text = "No Dart"
dart_images = []

# loop over the frames of the video
while True:
	# grab the current frame and initialize the output text
    ret, frame = capture.read()
    

    if frame is None:
        break
	
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
    if firstFrame is None:
        firstFrame = gray

        continue
    
    frameDelta = cv2.absdiff(firstFrame, gray)
      
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2) 
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    time_since_last_throw = round(time.time() - time_last_throw, 2)
    
    if time_since_last_throw > 2:
        
        print("Waiting for throw since " + str(time_since_last_throw))
        
        for c in cnts:
             
            if cv2.contourArea(c) < min_area:
                continue
            
            print("Dart detected with " +  str(cnts.count) + " Countour Areas: " + str(cv2.contourArea(c)) + "and " + str(time_since_last_throw))
            
            time_last_throw = time.time()
            
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            dart_counter = dart_counter + 1        
            
            #Set new first frame
            dart_images.append(frameDelta)
            firstFrame = gray
            
            text = str(dart_counter) + " darts thrown!"
            
            break
            
    else:
        
        print("Skipped detection!")







    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if dart_counter == 3:
        break
        
    
capture.release()
cv2.destroyAllWindows()

plt.close('all')
#%%

for image in dart_images:
    
    plt.figure()
    plt.imshow(image,cmap = 'gray')
    




import imutils
import cv2
from PIL import ImageTk, Image
import numpy as np
import time


class Dart_Detector():
    
    def __init__(self):
        
        
    






# Takes the image from the webcam, grayscales it, blurs it and saves 4 images: top_processed, right_processed, top_raw, right_raw
def process_frame(frame, blur):
    
    image_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                  #Grayscale
    image_processed = cv2.GaussianBlur(image_processed, (51, 51), 0)         #Blur
        
    t_image_processed = image_processed[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_processed = image_processed[int(image_processed.shape[0]/2) + 1 :,:]
    
    t_image_raw = frame[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_raw = frame[int(image_processed.shape[0]/2) + 1 :,:] 
    
    return t_image_processed, r_image_processed, t_image_raw, r_image_raw


# Calculates the differences between a background image and an image
def calc_background_dif(image, background_image, name, debug):
    
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
                
                if debug:
                
                    print(name + "  " +str(cv2.contourArea(con)))
                
                n_dif_pix.append(cv2.contourArea(con))
                
                            
        n_dif_pix_tot = sum(n_dif_pix)
    
    else:
        
        n_dif_pix_tot = 0
    
    if debug:

        cv2.imshow(name, debug_image)
    
    return n_dif_pix_tot, background_image
 
   
def resize_create(image, scale_percent): 
    
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image 
    resizedImage = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    
    photo = ImageTk.PhotoImage(image = Image.fromarray(resizedImage))
    
    return photo

def detect_darts(detection, time_last_throw, image, first_frame):
    
    if detection:
        
            ## Get pixel differences over the two pictures
            dif_pix, first_frame = calc_background_dif(image, first_frame, "TOP", False)
                       
            return dif_pix, first_frame
           
def count_darts(main, dart_counter, t_image_raw, r_image_raw, dif_pix):   


    main.time_last_throw = time.time()
    
    #Set the Background frames to None to force the app to get new images after the delay
    main.t_firstFrame = None
    main.r_firstFrame = None
    
    dart_counter = dart_counter + 1    
    
    main.text_display.print_to_display(str(dart_counter) + ". dart thrown: " + str(dif_pix) + " white pixels")
    
    if main.dart_counter == 3:
        
        main.t_dart_images.append(t_image_raw)
        main.r_dart_images.append(r_image_raw)
        
        
        main.detection = False
        main.text_display.print_to_display("Detection set to False, get the darts")
        
        main.time_start_throw = time.time()
        main.button_save_and_next.config(state = "normal")

    ##Delay a bit to get a still board again
    time.sleep(1)
    
    return dart_counter
 
def save_images(counter, ):


       

def outline_from_image(image, bw_threshold, cannyMin, cannyMax):


    image = cv2.blur(image,(6,6))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(image, bw_threshold, 255, cv2.THRESH_BINARY)
    image = cv2.Canny(blackAndWhiteImage, cannyMin, cannyMax)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    image = cv2.dilate(image, kernel)
    
    alphaRgb = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB) 
    
    image = cv2.bitwise_not(image)
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    
    colorRgb = image.copy()
    colorRgb[np.where((colorRgb==[0,0,0]).all(axis=2))] = [255,0,255]
    
    return colorRgb, alphaRgb
    
def add_outline_marker(background, foreground, alpha):

    foreground = foreground.astype(float)
    background = background.astype(float)
    alpha = alpha.astype(float)/255

	# Multiply the foreground with the alpha matte

    foreground = cv2.multiply(alpha, foreground)

	# Multiply the background with ( 1 - alpha )

    background = cv2.multiply(1.0 - alpha, background)

	# Add the masked foreground and background.
    outImage = cv2.add(background, foreground)

    # Convert back to uint8
    outImage = outImage.astype(np.uint8)

    return outImage    





import imutils
import cv2
from PIL import ImageTk, Image


#%% Functions

def process_frame(frame, blur):
    
    
    image_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      #Grayscale
    image_processed = cv2.GaussianBlur(image_processed, (51, 51), 0)         #Blur
        
    t_image_processed = image_processed[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_processed = image_processed[int(image_processed.shape[0]/2) + 1 :,:]
    
    t_image_raw = frame[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_raw = frame[int(image_processed.shape[0]/2) + 1 :,:] 
    
    return t_image_processed, r_image_processed, t_image_raw, r_image_raw


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
    
    
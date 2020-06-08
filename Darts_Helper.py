import cv2
from PIL import ImageTk, Image
import numpy as np



# Takes the image from the webcam, grayscales it, blurs it and saves 4 images: top_processed, right_processed, top_raw, right_raw
def process_frame(frame, blur):
    
    image_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                  #Grayscale
    image_processed = cv2.GaussianBlur(image_processed, (51, 51), 0)         #Blur
        
    t_image_processed = image_processed[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_processed = image_processed[int(image_processed.shape[0]/2) + 1 :,:]
    
    t_image_raw = frame[0: int(image_processed.shape[0]/2),:]      #Split into top and right camera image
    r_image_raw = frame[int(image_processed.shape[0]/2) + 1 :,:] 
    
    return t_image_processed, r_image_processed, t_image_raw, r_image_raw

   
def resize_create(image, scale_percent): 
    
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image 
    resizedImage = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
    
    photo = ImageTk.PhotoImage(image = Image.fromarray(resizedImage))
    
    return photo


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





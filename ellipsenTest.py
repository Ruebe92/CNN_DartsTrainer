import cv2
import dartshelper as dh
import numpy as np
  
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
    

#%%

url = "http://192.168.0.42:8000/video_feed"
capture = cv2.VideoCapture(url)

r_background = cv2.imread('r_image_raw_baseline.jpg')
t_background = cv2.imread('t_image_raw_baseline.jpg')

colorRgb, alphaRgb = outline_from_image(t_background, 180, 300, 500)


#%%

# loop over the frames of the video
while True:
 	
    ret, frame = capture.read()
    
    if ret:
        
        t_image, r_image, t_image_raw, r_image_raw = dh.process_frame(frame, 31)
        
        outimage = add_outline_marker(t_image_raw, colorRgb, alphaRgb)
        
        cv2.imshow("outy", outimage)

        
        
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
    

cv2.destroyAllWindows()
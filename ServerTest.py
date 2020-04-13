import cv2

def canny(img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        kernel = 5
        blur = cv2.GaussianBlur(gray,(kernel, kernel),0)
        canny = cv2.Canny(blur, 50, 150)
        return canny


def grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def equalize(img):
    img = cv2.equalizeHist(img)
    return img

def preprocessing(img):
    img = canny(img) 
    #img = grayscale(img)
    #img = equalize(img)    
    img = img/255  

    return img

capture = cv2.VideoCapture('http://pi:raspberry@192.168.0.40:8081')

while(True):
    
    # Capture frame-by-frame
    ret, frame = capture.read()
    
    if ret == False:
        
        print( "Could not get video source")
        break
    
    
    frame_processed = preprocessing(frame)
    frame_original = preprocessing(frame)
    
    frame = cv2.hconcat((frame, frame))
    
    # Display the resulting frame
    cv2.imshow('Live Dartboard - Unten rechts',frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
import imutils
import cv2
import time
import numpy as np

class Dart_Detector():
    
    def __init__(self, main):
        
        self.main = main
        self.detection = True
        
        self.time_threshold = 0.5
        self.delay_after_shot = 0.35
        self.peak_dif_pix = 0
        
        self.t_image_raw = []
        self.r_image_raw = []
        
        self.time_array = []
        self.pix_array = []
        self.thresh_array = []
        
        self.first_frame_top = None
        self.first_frame_right = None
        
        self.image_result = []
        self.time_plus_delay = []
        self.delay_flag = False
        self.abs_delay_time = 1000
        
        

    def detect(self):
        
        if self.detection == True:
            
            
            time_since_last_throw = round(time.time() - self.main.time_last_throw, 2)
                
            dif_pix_top, self.main.first_frame_top = self.calc_background_dif(self.main.image_top, self.main.first_frame_top, self.main.image_raw_top)    
            dif_pix_right, self.main.first_frame_right = self.calc_background_dif(self.main.image_right, self.main.first_frame_right, self.main.image_raw_right)

            self.dif_pix = dif_pix_top + dif_pix_right  
            
            if self.dif_pix > self.peak_dif_pix:
                
                self.peak_dif_pix = self.dif_pix
                

            self.min_pix = self.main.frame_UI_right.scale_min_pix.get()
            
            if self.dif_pix > self.min_pix and self.delay_flag == False:
                
                self.delay_flag = True
                self.abs_delay_time = time.time() + self.delay_after_shot
                self.draw_shot(time.time(),'b')
                
                
            if time.time() > self.abs_delay_time and self.delay_flag == True:
                
                self.delay_flag = False
                
                
                self.collect_images()
                self.count_darts()       
                self.peak_dif_pix = 0         
                
                self.draw_shot(time.time(),'g')
                
                self.reset_images()
                
                
                
                
            # Save to array for debugging & plotting
            self.time_array.append(time.time())                 
            self.pix_array.append(self.dif_pix)
            self.thresh_array.append(self.min_pix)
            
            

    def reset_images(self):
        #Set the Background frames to None to force the app to get new images after the delay
        self.main.first_frame_top = None
        self.main.first_frame_right = None
        self.main.first_frame_top_raw = None
        self.main.first_frame_right_raw = None
        
            
            


    
    
    def collect_images(self):
        
        image_top_before = self.main.first_frame_top[1]
        image_right_before = self.main.first_frame_right[1]
        
        image_top_shot = self.main.image_raw_top
        image_right_shot = self.main.image_raw_right
        
        image_part_left = np.concatenate((image_top_before, image_right_before), axis=0)
        image_part_right = np.concatenate((image_top_shot, image_right_shot), axis=0)

        image_result = np.concatenate((image_part_left, image_part_right), axis=1)
        
        scale_percent = 50
        width = int(image_result.shape[1] * scale_percent / 100)
        height = int(image_result.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image 
        
        temp_result = cv2.resize(image_result, dim, interpolation = cv2.INTER_AREA)
        
        self.image_result.append(temp_result)
        
        #cv2.imshow(str(self.main.dart_count), temp_result)
        
                 
        
    def count_darts(self):   


        self.main.time_last_throw = time.time()
        
        self.main.dart_count += 1   
        
        self.main.text_display.print_to_display(str(self.main.dart_count) + ". dart thrown: " + str(self.dif_pix) + " white pixels")
        
        if self.main.dart_count == 3:
            
            self.detection = False
            self.main.text_display.print_to_display("Detection set to False, get the darts")
            
            self.main.time_start_throw = time.time()
            self.main.frame_UI_left.button_save_and_next.config(state = "normal")
    
        
        
 
    
    def calc_background_dif(self,image, first_frame, image_raw):
    
        if first_frame is None:
            
            first_frame = []
            first_frame.append(image)
            first_frame.append(image_raw)

            
        frameDelta = cv2.absdiff(first_frame[0], image)
        
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
                    
                    n_dif_pix.append(cv2.contourArea(con))
                    
                                
            n_dif_pix_tot = sum(n_dif_pix)
        
        else:
            
            n_dif_pix_tot = 0
        
        
        return n_dif_pix_tot, first_frame
            
        
    def draw_detection_plot(self):
            
        self.main.frame_UI_right.ax.plot(self.time_array, self.thresh_array, linestyle = '-', marker = 'None', color='green', label= "Treshold")
        self.main.frame_UI_right.ax.plot(self.time_array, self.pix_array, linestyle = '-', marker = 'None', color='red', label= "Pixels")
        self.main.frame_UI_right.graph.draw()
        
        
    def draw_shot(self, time, color):
        
        self.main.frame_UI_right.ax.axvline(x = time, color= color)
            
            
    def reset(self):
        
        self.t_image_raw = []
        self.r_image_raw = []
        
        self.time_array = []
        self.pix_array = []
        self.thresh_array = []
        
        self.main.frame_UI_right.ax.cla()
        
        
    


       







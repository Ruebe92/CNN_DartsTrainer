# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 00:09:16 2020

@author: ShortyP
"""

class dartsGUI:

    def __init__(self, window, window_title):
        
            window.geometry("1280x840")    
            
            window.resizable(0, 0)
            
            self.window = window
            
            self.window.title(window_title)
        
            self.create_board_canvas()
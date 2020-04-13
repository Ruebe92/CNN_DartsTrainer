import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import tkinter

#Dartboard-Dimensions
def Draw_Dartboard():
    
    r_full = 45.5/2
    r_inner_triple = 19.3/2
    r_outer_triple = 21.3/2
    r_inner_double = 32.0/2
    r_outer_double = 34.0/2
    r_outer_rim = 40.0/2
    
    
    board_full = plt.Circle((0, 0), r_full, color='k', zorder = 0)
    
    inner_triple = plt.Circle((0, 0), r_inner_triple, color='w', zorder = 0)
    outer_triple = plt.Circle((0, 0), r_outer_triple, color='g', zorder = 0)
    
    inner_double = plt.Circle((0, 0), r_inner_double, color='w', zorder = 0)
    outer_double = plt.Circle((0, 0), r_outer_double, color='g', zorder = 0)
    
    double_Bull = plt.Circle((0, 0), 1.4/2, color='r', zorder = 3)
    single_Bull = plt.Circle((0, 0), 3.3/2, color='g', zorder = 2)
    
    arc = patches.Arc((0,0),0, 100, angle= 10, theta1=3 , theta2=360.0)
    
    
    fig, ax = plt.subplots()
    
    plt.axis('scaled')
    
    ax.add_artist(board_full)
    ax.add_artist(outer_double)
    ax.add_artist(inner_double)
    ax.add_artist(outer_triple)
    ax.add_artist(inner_triple)
    
    #angle = - (360/20/2)
        
    #x = math.cos(math.radians(angle)) * r_outer_double
    #y = math.sin(math.radians(angle)) * r_outer_double
    
    #plt.plot([0, x], [0, y], color='k', linestyle='-', linewidth=2, zorder = 1)
    
    field_number = ["6","13","4","18","1","20","5","12","9","14","11","8","16","7","19","3","17","2","15","10"]
    
    
    for seg in range(20):
        
        angle1 = 360/20 * seg - (360/20/2)
        x1 = math.cos(math.radians(angle1)) * r_outer_double
        y1 = math.sin(math.radians(angle1)) * r_outer_double
        
        plt.plot([0, x1], [0, y1], color='k', linestyle='-', linewidth=2, zorder = 1)
        
        angle_text = 360/20 * seg
        
        x_text = math.cos(math.radians(angle_text)) * r_outer_rim
        y_text = math.sin(math.radians(angle_text)) * r_outer_rim
    
        plt.text(x_text, y_text, field_number[seg], size=10, rotation=0, ha="center", va="center", color='white', fontsize=20)
    
    ax.add_artist(single_Bull)
    ax.add_artist(double_Bull)
    
    ax.axis(xmin=-30,xmax=30)
    ax.axis(ymin=-30,ymax=30)
    
    
    return fig, ax





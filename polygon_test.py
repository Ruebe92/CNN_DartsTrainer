import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np
import math
import tkinter


def draw_segment(seg):
    
    if (seg % 2) == 0 or seg == 0:
        
        mainColor = 'k'
        secondColor = 'r'
        
    else: 
        
        mainColor = 'w'
        secondColor = 'g'
        
    angle = 360/20 * seg
    
    angle1 = angle - (360/20/2)
    angle2 = angle + (360/20/2)   
     
    angles = np.linspace(angle1, angle2, num=200)
    
    coordinates = []
    coordinates.append([0,0])
    
    for angle in angles:
        
        x = math.cos(math.radians(angle)) * r_outer_double
        y = math.sin(math.radians(angle)) * r_outer_double
    
        coordinates.append([x,y])
    
    coordinates.append([0,0])
    
    xy  = np.asarray(coordinates)
    
    patch = patches.Polygon(xy, color = mainColor)
    
    ax.add_artist(patch)
    
    #%%
    coordinates = []
    
    for angle in reversed(angles):
        
        x = math.cos(math.radians(angle)) * r_inner_double
        y = math.sin(math.radians(angle)) * r_inner_double
    
        coordinates.append([x,y])
    
    for angle in angles:
        
        x = math.cos(math.radians(angle)) * r_outer_double
        y = math.sin(math.radians(angle)) * r_outer_double
    
        coordinates.append([x,y])
    
    xy  = np.asarray(coordinates)
    
    patch = patches.Polygon(xy, color = secondColor)
    
    ax.add_artist(patch)
    
    #%%
    
    coordinates = []
    
    for angle in reversed(angles):
        
        x = math.cos(math.radians(angle)) * r_inner_triple
        y = math.sin(math.radians(angle)) * r_inner_triple
    
        coordinates.append([x,y])
    
    for angle in angles:
        
        x = math.cos(math.radians(angle)) * r_outer_triple
        y = math.sin(math.radians(angle)) * r_outer_triple
    
        coordinates.append([x,y])
    
    xy  = np.asarray(coordinates)
    
    patch = patches.Polygon(xy, color = secondColor)
    
    ax.add_artist(patch)



    
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


fig = plt.figure(figsize = (2.5,2.5))

ax = fig.add_subplot(111)
    
ax.add_artist(board_full)
ax.add_artist(outer_double)
ax.add_artist(inner_double)
ax.add_artist(outer_triple)
ax.add_artist(inner_triple)


field_number = ["6","13","4","18","1","20","5","12","9","14","11","8","16","7","19","3","17","2","15","10"]


for seg in range(20):
    
    draw_segment(seg)
    
    angle_text = 360/20 * seg
    
    x_text = math.cos(math.radians(angle_text)) * r_outer_rim
    y_text = math.sin(math.radians(angle_text)) * r_outer_rim

    plt.text(x_text, y_text, field_number[seg], size=10, rotation=0, ha="center", va="center", color='white', fontsize=20)

ax.add_artist(single_Bull)
ax.add_artist(double_Bull)

ax.axis(xmin=-30,xmax=30)
ax.axis(ymin=-30,ymax=30)




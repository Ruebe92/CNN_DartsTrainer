import tkinter as tk
from random import randint
 
# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading
 
continuePlotting = False
 
def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True
    
 
def data_points():
    f = open("data.txt", "w")
    for i in range(10):
        f.write(str(randint(0, 10))+'\n')
    f.close()
 
    f = open("data.txt", "r")
    data = f.readlines()
    f.close()
 
    l = []
    for i in range(len(data)):
        l.append(int(data[i].rstrip("\n")))
    return l
 
def app():
    # initialise a window.
    root = tk.Tk()
    root.config(background='white')
    root.geometry("1000x700")
    
    lab = tk.Label(root, text="Live Plotting", bg = 'white').pack()
    
    fig = Figure()
    
    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()
 
    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top",fill='both',expand=True)
 
    def plotter():
        
        ax.cla()
        ax.grid()
        dpts = data_points()
        ax.plot(range(10), dpts, marker='o', color='orange')
        graph.draw()

        
        root.after(delay, plotter)
 
    
    delay = 1
    
    
    plotter()
        
        
                
    root.mainloop()
 
if __name__ == '__main__':
    app()
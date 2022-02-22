import tkinter as tk
from PIL import Image, ImageTk
import imageHybrid
import cv2
import numpy as np
import imageFuncs as imf
import pagination
import threading
import time 

window = tk.Tk()

coefficient = 0.05
height = 600
width = 600


greeting = tk.Label(text="Hybrid Image")

greeting.pack()

#imgHi = cv2.resize(cv2.imread("TestImages/Dogge.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
document = pagination.readDocument("TestDoc1.hpd")
imgHi, docIdx, docEnd = pagination.generatePage(document, 0)
imgHi = imgHi.astype('float64')/256
imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)
img =  imf.readyImageForCanvas(picture)

canvas = tk.Canvas(window,width=600,height=600)
canvas.pack()
canvasImage = canvas.create_image(20,20, anchor="nw", image=img)

def switchLowImage(val):
    global imgLo
    if val == 'cat':
        imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
    if val == 'noise':
        imgLo = np.zeros((width, height,3))
        ch1 = np.random.rand(width,height)
        imgLo[:,:,0] = ch1
        imgLo[:,:,1] = ch1
        imgLo[:,:,2] = ch1


def setCoeff(value):
    global coefficient
    coefficient = float(value)

s1 = tk.Scale(window, from_=0, to=1, length=600,resolution=0.01, orient=tk.HORIZONTAL, command=setCoeff).pack(pady= 20)

def refreshImage():
    global img
    global s1
    global coefficient
    while 1:
        picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)
        newimg = imf.readyImageForCanvas(picture)
        canvas.itemconfig(canvasImage, image = newimg)
        img = newimg
        canvas.itemconfig(canvasImage, image = img)        
        #time.sleep(0.2)



threading.Thread(target=refreshImage).start()

tk.Button(window, text= "cat", command= lambda: switchLowImage('cat')).pack(pady= 20)
tk.Button(window, text= "noise", command= lambda:switchLowImage('noise')).pack(pady= 20)

window.mainloop()

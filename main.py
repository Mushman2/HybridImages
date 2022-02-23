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
filterMode = 0






#imgHi = cv2.resize(cv2.imread("TestImages/Dogge.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
document = pagination.readDocument("TestDoc1.hpd")
imgHi, docIdx, docEnd = pagination.generatePage(document, 0)
imgHi = imgHi.astype('float64')/256
imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)
img =  imf.readyImageForCanvas(picture)

canvas = tk.Canvas(window,width=600,height=600)
canvas.pack(side = tk.TOP)
canvasImage = canvas.create_image(20,20, anchor="nw", image=img)

def setCoeff(value):
    global coefficient
    coefficient = float(value)

s1 = tk.Scale(window, from_=0, to=1, length=600,resolution=0.01, orient=tk.HORIZONTAL, command=setCoeff).pack(pady= 5)

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

bgFrame = tk.Frame(window)
bgFrame.pack(pady= 2)
tk.Label(bgFrame, text="Background").grid(row = 0, column = 0)
tk.Button(bgFrame, text= "Cat", command= lambda: switchLowImage('cat')).grid(row = 0, column = 1)
tk.Button(bgFrame, text= "Noise", command= lambda:switchLowImage('noise')).grid(row = 0, column = 2)

def setMode(mode):
    global filterMode
    filterMode = mode

algFrame = tk.Frame(window)
algFrame.pack(pady= 2)
tk.Label(algFrame, text="Algorithm").grid(row = 0, column = 0)
tk.Button(algFrame, text= "Fourier", command= lambda: setMode(0)).grid(row = 0, column = 1)
tk.Button(algFrame, text= "Gauss", command= lambda:setMode(1)).grid(row = 0, column = 2)
tk.Button(algFrame, text= "Sobel", command= lambda:setMode(2)).grid(row = 0, column = 3)

def refreshImage():
    global img
    global s1
    global coefficient
    while 1:
        if filterMode == 0: 
            picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)            
        elif filterMode == 1:
            picture = imageHybrid.gaussianHybrid(imgLo,imgHi,coefficient)
        else: 
            picture = imageHybrid.sobelHybrid(imgLo,imgHi,coefficient)

        newimg = imf.readyImageForCanvas(picture)
        canvas.itemconfig(canvasImage, image = newimg)
        img = newimg
        canvas.itemconfig(canvasImage, image = img)        
        #time.sleep(0.2)

threading.Thread(target=refreshImage).start()
window.mainloop()

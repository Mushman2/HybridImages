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
shape = 'square'

#imgHi = cv2.resize(cv2.imread("TestImages/Dogge.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
document = pagination.readDocument("TestDoc1.hpd")
imgHi, docIdx, docEnd = pagination.generatePage(document, 0)
imgHi = imgHi.astype('float64')/256
imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient,shape)
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
    if val == 's&p':
        imgLo = np.zeros((width, height,3))
        ch1 = np.random.randint(2, size = (width, height))
        imgLo[:,:,0] = ch1
        imgLo[:,:,1] = ch1
        imgLo[:,:,2] = ch1
    if val == 'grey':
        imgLo = np.zeros((width, height,3))
        imgLo += 0.5

def generateSaliencyImage():
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(np.float32(picture[:,:,0]))
    saliencyMap = (saliencyMap * 255).astype("uint8")
    cv2.imshow("Image", picture)
    cv2.imshow("Output", saliencyMap)
    cv2.waitKey(0)
    return

bgFrame = tk.Frame(window)
bgFrame.pack(pady= 2)
tk.Label(bgFrame, text="Background").grid(row = 0, column = 0)
tk.Button(bgFrame, text= "Cat", command= lambda: switchLowImage('cat')).grid(row = 0, column = 1)
tk.Button(bgFrame, text= "Noise", command= lambda:switchLowImage('noise')).grid(row = 0, column = 2)
tk.Button(bgFrame, text= "S&P", command= lambda:switchLowImage('s&p')).grid(row = 0, column = 3)
tk.Button(bgFrame, text= "Grey", command= lambda:switchLowImage('grey')).grid(row = 0, column = 4)

def setMode(mode):
    global filterMode
    filterMode = mode

algFrame = tk.Frame(window)
algFrame.pack(pady= 2)
tk.Label(algFrame, text="Algorithm").grid(row = 0, column = 0)
tk.Button(algFrame, text= "Fourier - SQ", command= lambda: setMode(0)).grid(row = 0, column = 1)
tk.Button(algFrame, text= "Gauss", command= lambda:setMode(1)).grid(row = 0, column = 2)
tk.Button(algFrame, text= "Fourier - CI", command= lambda:setMode(2)).grid(row = 0, column = 3)

salFrame = tk.Frame(window)
salFrame.pack(pady=2)
tk.Button(salFrame, text = "Generate Saliency Image", command=generateSaliencyImage ).grid(row = 0, column = 0)

def refreshImage():
    global img
    global s1
    global coefficient
    global shape
    global picture
    while 1:
        if filterMode == 0: 
            picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient,"square")            
        elif filterMode == 1:
            picture = imageHybrid.gaussianHybrid(imgLo,imgHi,coefficient)
        else: 
            picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient, "circle")

        newimg = imf.readyImageForCanvas(picture)
        canvas.itemconfig(canvasImage, image = newimg)
        img = newimg
        canvas.itemconfig(canvasImage, image = img)        
        #time.sleep(0.2)

threading.Thread(target=refreshImage).start()
window.mainloop()

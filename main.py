import tkinter as tk
from PIL import Image, ImageTk
import imageHybrid
import cv2
import numpy as np
import imageFuncs as imf
import pagination

window = tk.Tk()

coefficient = 0.05

greeting = tk.Label(text="Hybrid Image")

greeting.pack()

#imgHi = cv2.resize(cv2.imread("TestImages/Dogge.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
document = pagination.readDocument("TestDoc1.hpd")
imgHi, docIdx = pagination.generatePage(document, 0)
imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)
img =  imf.readyImageForCanvas(picture)

canvas = tk.Canvas(window,width=600,height=600)
canvas.pack()
canvasImage = canvas.create_image(20,20, anchor="nw", image=img)

def refreshImage(change):
    global coefficient
    global img

    coefficient += change
    picture = imageHybrid.fourierHybrid(imgLo,imgHi,coefficient)
    img = imf.readyImageForCanvas(picture)
    canvas.itemconfig(canvasImage, image = img)

tk.Button(window, text= "N+", command= lambda: refreshImage(0.01)).pack(pady= 20)
tk.Button(window, text= "N-", command= lambda: refreshImage(-0.01)).pack(pady= 20)
window.mainloop()
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

def readDocument(name):
    file1 = open(name, 'r')
    Lines = file1.readlines()
    document = []

    for line in Lines:
        document.extend(line.strip().split())
        document.append("\n")
    return document

def generatePage(document, index):
    height = 600
    width = 600

    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    thickness = 1
    colour = (255,255,255)

    image = np.zeros(width,height,3)
    currentIndex = index

    full = False
    heightPointer = 10
    widthPointer = 10
    while (not full):
        size = cv2.getTextSize(document[currentIndex], font, fontScale, thickness)
        if widthPointer + size.width < width - 10:
            image = cv2.putText(image, document[currentIndex], (widthPointer, heightPointer), font, fontScale, colour, thickness, cv2.LINE_AA)
            widthPointer += size.width + 10
        else:
            heightPointer += size.height + 10
            widthPointer = 10
            if heightPointer + size.height < height - 10:
                image = cv2.putText(image, document[currentIndex], (widthPointer, heightPointer), font, fontScale, colour, thickness, cv2.LINE_AA)
            else:
                full = True
    return image, currentIndex



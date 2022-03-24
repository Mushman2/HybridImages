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

    image = np.zeros((width,height,3))
    currentIndex = index

    full = False
    docEnd = False
    heightPointer = 10 + cv2.getTextSize(document[currentIndex], font, fontScale, thickness)[0][1]
    widthPointer = 10
    while (not full):
        if currentIndex == len(document):
            full = True
            docEnd = True
        elif (document[currentIndex] == '\n'):
            heightPointer += size[0][1] + 10
            widthPointer = 10   
            currentIndex += 1
            fontScale = 1
            thickness = 1
        elif ((document[currentIndex] == '^')):
            currentIndex += 1
            fontScale = 1.5
        else:        
            word = document[currentIndex]
            if word[0] == "*":
                thickness = 2
                word = word[1:]
            else:
                thickness = 1
            size = cv2.getTextSize(word, font, fontScale, thickness)
            if (widthPointer + size[0][0]) < (width - 10):
                image = cv2.putText(image, word, (widthPointer, heightPointer), font, fontScale, colour, thickness, cv2.LINE_AA)
                widthPointer += size[0][0] + 10
                currentIndex += 1
            else:
                heightPointer += size[0][1] + 10
                widthPointer = 10
                if heightPointer + size[0][1] < height - 10:
                    image = cv2.putText(image, word, (widthPointer, heightPointer), font, fontScale, colour, thickness, cv2.LINE_AA)
                    widthPointer += size[0][0] + 10
                    currentIndex += 1
                else:
                    full = True

    return image, currentIndex, docEnd



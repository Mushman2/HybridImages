from PIL import Image, ImageTk
import cv2
import numpy as np

def readyImageForCanvas(picture):
    picture[picture > 1] = 1
    picture[picture < 0] = 0
    intPicture = ((picture * 200)+5).astype(np.uint8)
    intPicture = cv2.cvtColor(intPicture, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(image=Image.fromarray(intPicture))
    return img

from PIL import Image, ImageTk
import cv2
import numpy as np

def generateMask(width, height, shape, n):
    mask = np.zeros((width, height, 3), dtype=np.csingle)
    half_w, half_h = int(width/2), int(height/2)
    nh = int(n/2*height)
    nw = int(n/2*width)
    if shape == 'square':
        mask [half_w-nw:half_w+nw+1,half_h-nh:half_h+nh+1] = 1
    elif shape == 'circle':
        Y, X = np.ogrid[:height, :width]
        center = (int(width/2), int(height/2))
        radius = int(n/2*height)
        dist_from_center = np.repeat(np.sqrt((X - center[0])**2 + (Y-center[1])**2).reshape(width, height, 1), 3, axis = 2)
        
        mask = dist_from_center <= radius
    return mask

def readyImageForCanvas(picture):
    picture[picture > 1] = 1
    picture[picture < 0] = 0
    intPicture = ((picture * 200)+5).astype(np.uint8)
    intPicture = cv2.cvtColor(intPicture, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(image=Image.fromarray(intPicture))
    return img

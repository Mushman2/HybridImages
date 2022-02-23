import numpy as np
import cv2
import textwrap 
from skimage.io import imread
import matplotlib.pyplot as plt
import scipy.fft as fp
from skimage.util import random_noise
from scipy import ndimage

#Combine 2 equally sized images into a hybrid image

#Combine using fourier transform low and high pass filters
def fourierHybrid(imageLow, imageHigh, n):
    #cv2.imshow("imgHi",imageHigh)
    #cv2.imshow("imgLo", imageLow)
    #cv2.waitKey(0)

    FHi = np.zeros(imageHigh.shape, dtype=np.csingle)
    FLo = np.zeros(imageLow.shape, dtype=np.csingle)
    for channel in range(3): 
        FHi[:,:,channel] = fp.fftshift(fp.fft2((imageHigh[:,:,channel])))
        FLo[:,:,channel] = fp.fftshift(fp.fft2((imageLow[:,:,channel])))

    #plt.figure(figsize=(10,10))
    #plt.imshow( (20*np.log10( 0.1 + FHi)).astype(int))
    #plt.show()

    (w, h) = imageHigh.shape[:2]
    half_w, half_h = int(w/2), int(h/2)
    nh = int(n/2*h)
    nw = int(n/2*w)
    # high pass filter - Square
    FHi[half_w-nw:half_w+nw+1,half_h-nh:half_h+nh+1] = FLo[half_w-nw:half_w+nw+1,half_h-nh:half_h+nh+1] # select all but the first 50x50 (low) frequencies
    #plt.figure(figsize=(10,10))
    #plt.imshow( (20*np.log10( 0.1 + FHi)).astype(int))
    #plt.show()

    imHi1 = np.zeros(imageHigh.shape, dtype=np.float64)
    for channel in range(3): 
        imHi1[:,:,channel] = fp.ifft2(fp.ifftshift(FHi[:,:,channel])).real#.astype(np.uint8)

    #cv2.imshow("img2",imHi1)
    #cv2.imshow("testfft", fp.ifft2(fp.ifftshift(fp.fftshift(fp.fft2(imageHigh[:,:,0])))).real)#.astype(np.uint8))
    #cv2.waitKey(0)
    return imHi1

def sobelHybrid(imageLow, imageHigh, n):
    #TODO: Gaussian Blur both images.
    lowpass = ndimage.gaussian_filter(imageLow, 2-2*n)

    dx = ndimage.sobel(imageHigh, 0)  
    dy = ndimage.sobel(imageHigh, 1)  
    hipass = np.hypot(dx, dy)
    #TODO: Perfom subtraction for high pass image
    #TODO: Combine Images
    return lowpass + hipass

def gaussianHybrid(imageLow, imageHigh, n):
    #TODO: Gaussian Blur both images.
    lowpass = ndimage.gaussian_filter(imageLow, 2-2*n)
    hiImgLowPass = ndimage.gaussian_filter(imageHigh, 2-2*n)
    #TODO: Perfom subtraction for high pass image
    hipass = imageHigh - hiImgLowPass
    #TODO: Combine Images
    return lowpass + hipass

import numpy as np
import cv2
import textwrap 
from skimage.io import imread
import matplotlib.pyplot as plt
import scipy.fft as fp
from skimage.util import random_noise
from scipy import ndimage
import imageFuncs

maskCache = mask = np.zeros((600, 600, 3), dtype=np.csingle)
nCache = -1
n2Cache = -1
shapeCache = -1


#Combine 2 equally sized images into a hybrid image
def hybridImg(imgLow, imgHigh, mode, n1, n2):
    if mode == 'gauss':
        return gaussianHybrid(imgLow, imgHigh, n1, n2)
    else:
        return fourierHybrid(imgLow, imgHigh, n1, n2, mode)  


#Combine using fourier transform low and high pass filters
def fourierHybrid(imageLow, imageHigh, n, n2, shape):
    global maskCache, nCache, n2Cache, shapeCache
    #return imageHigh
    FHi = np.zeros(imageHigh.shape, dtype=np.csingle)
    FLo = np.zeros(imageLow.shape, dtype=np.csingle)
    for channel in range(3): 
        FHi[:,:,channel] = fp.fftshift(fp.fft2((imageHigh[:,:,channel])))
        FLo[:,:,channel] = fp.fftshift(fp.fft2((imageLow[:,:,channel])))
    #return FLo.real/ 255
    (w, h) = imageHigh.shape[:2]
    if nCache == n and n2Cache == n2 and shapeCache == shape:
        mask = maskCache
    else:
        mask = imageFuncs.generateMask(w,h,shape,n, n2)
        maskCache = mask
        nCache = n
        n2Cache = n2
        shapeCache = shape
    #return mask.real
    FHi = (FHi * (1 - mask)) + (FLo * (mask))
    #return FHi.real / 255
    imHi1 = np.zeros(imageHigh.shape, dtype=np.float64)
    for channel in range(3): 
           imHi1[:,:,channel] = fp.ifft2(fp.ifftshift(FHi[:,:,channel])).real#.astype(np.uint8)

    #return FHi.real / 255
    return imHi1

#Combine using gaussian blur high and low pass filters
def gaussianHybrid(imageLow, imageHigh, n, n2): 
    #Sigma = 3 seems like a reasonable maximum
    scaling = 3
    sigma = scaling-scaling*n
    sigma2 = scaling-scaling*n2
    #Gaussian Blur both images.
    lowpass = ndimage.gaussian_filter(imageLow, sigma=(sigma,sigma,0))

    hiImgLowPass = ndimage.gaussian_filter(imageHigh, sigma=(sigma2,sigma2,0))
  
    #Perfom subtraction for high pass image
    hipass = imageHigh - hiImgLowPass
    #return hiImgLowPass      
    #Combine Images
    return lowpass + hipass

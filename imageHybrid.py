import numpy as np
import cv2
import textwrap 
from skimage.io import imread
import matplotlib.pyplot as plt
import scipy.fft as fp
from skimage.util import random_noise
from scipy import ndimage
import imageFuncs

#Combine 2 equally sized images into a hybrid image
def hybridImg(imgLow, imgHigh, mode, n1, n2):
    if mode == 'gauss':
        return gaussianHybrid(imgLow, imgHigh, n1, n2)
    else:
        return fourierHybrid(imgLow, imgHigh, n1, n2, mode)  


#Combine using fourier transform low and high pass filters
def fourierHybrid(imageLow, imageHigh, n, n2, shape):
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
    mask = imageFuncs.generateMask(w,h,shape,n, n2)
    FHi = (FHi * (1 - mask)) + (FLo * (mask))
    

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

def gaussianHybrid(imageLow, imageHigh, n, n2):
    sigma = 2-2*n
    sigma2 = 2-2*n2
    #TODO: Gaussian Blur both images.
    lowpass = ndimage.gaussian_filter(imageLow, sigma=(sigma,sigma,0))
    hiImgLowPass = ndimage.gaussian_filter(imageHigh, sigma=(sigma2,sigma2,0))
    #TODO: Perfom subtraction for high pass image
    hipass = imageHigh - hiImgLowPass
    #TODO: Combine Images
    return lowpass + hipass

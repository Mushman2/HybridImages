import numpy as np
import cv2
import textwrap 
from skimage.io import imread
import matplotlib.pyplot as plt
import scipy.fft as fp
import imageHybrid

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Write some Text

font = cv2.FONT_HERSHEY_TRIPLEX
text = 'Somebody once told me the world was gonna roll me / I aint the sharpest tool in the shed'

wrapped_text = textwrap.wrap(text, width=25)
x, y = 10, 40
font_size = 1
font_thickness = 2

for i, line in enumerate(wrapped_text):
    textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]

    gap = textsize[1] + 10

    y = int((img.shape[0] + textsize[1]) / 2) + i * gap
    x = int((img.shape[1] - textsize[0]) / 2)

    cv2.putText(img, line, (x, y), font,
                font_size, 
                (255,255,255), 
                font_thickness, 
                lineType = cv2.LINE_AA)

imgHi = cv2.resize(cv2.imread("TestImages/Dogge.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
imgLo = cv2.resize(cv2.imread("TestImages/Catte.jpg"), (600,600), interpolation = cv2.INTER_NEAREST).astype('float64')/256
imageHybrid.fourierHybrid(imgLo,imgHi,0.05)
exit()

#Display the image
cv2.imshow("img",img)


F1 = fp.fft2((img).astype(float))
F2 = fp.fftshift(F1)
plt.figure(figsize=(10,10))
plt.imshow( (20*np.log10( 0.1 + F2)).astype(int), cmap=plt.cm.gray)
plt.show()

(w, h) = img.shape
half_w, half_h = int(w/2), int(h/2)

# high pass filter
n = 50
F2[half_w-n:half_w+n+1,half_h-n:half_h+n+1] = 0 # select all but the first 50x50 (low) frequencies
plt.figure(figsize=(10,10))
plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
plt.show()

im1 = fp.ifft2(fp.ifftshift(F2)).real
plt.figure(figsize=(10,10))
plt.imshow(im1, cmap='gray')
plt.axis('off')
plt.show()

# Add salt-and-pepper noise to the image.
noise_img = random_noise(im1, mode='gaussian')
plt.figure(figsize=(10,10))
plt.imshow(noise_img, cmap='gray')
plt.axis('off')
plt.show()


#Save image
cv2.imwrite("out.jpg", img)

cv2.waitKey(0)
#!/usr/bin/env python

'''
Kidprint Video Capture

Usage:
    KP_VideoCapture.py [--shotdir <shot path>]
Keys:
    ESC    - exit
    SPACE  - capture the image
    h      - switch file name --> hands
    z      - switch file name --> fingers
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np

#from skimage.filters import sobel_v, sobel_h
#from skimage import draw
#from skimage.exposure import equalize_hist

displayx = 1024.0     # x-direction display resolution
focusWindow = 0.2     # relative size of focus window
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
burstCount = 1

# Some flags
doBurst = False

def create_capture(size = "3840x2160"):
    '''size=<value>
    '''

    size = str(size).strip()
    cap = cv2.VideoCapture(0)
    w, h = map(int, size.split('x'))
    # The Size of the camera frames...
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
    return w, h, cap

# Show the histogram of the image

bins = np.arange(256).reshape(256, 1)

def hist_curve(im):
    h = np.zeros((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
            hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.int32(np.column_stack((bins,hist)))
            cv2.polylines(h,[pts],False,col)
            y=np.flipud(h)
    return y

# Canny Edge Detection Metheod to determine the Frame Focus Performance
def rateFrame(img):
    s = 0
    size = img.shape[1] * img.shape[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)
    #cv2.imshow("Gaussian", img)
    img = cv2.Canny(img, 0, 30, 3)
    cv2.imshow("Canny", img)
    s = np.sum(img)
    return s / float(size)

# Algorithn from Staal
def patch_angle(img, magnitude = True, tol = np.pi/8):
    '''return patch orientation in radians
     quality then compute the fraction of pixel gradient
    magnitude that is in the approximate orientation of the computed angle'''
    s = 0
    size = img.shape[1] * img.shape[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = equalize_hist(img)
    cv2.imshow("Equalized", img)

    gx = sobel_v(img)
    gy = sobel_h(img)

    vx = np.sum(2. * gx * gy)
    vy = np.sum(gx*gx - gy*gy)
    angle = (np.arctan2(vx,vy)/2) % np.pi

    if magnitude:
        magnitudes = np.hypot(gy, gx)
        angles = np.arctan2(gy, gx) % np.pi #
        omag = magnitudes[np.abs(angles - angle) < tol].sum()
        return angle, omag

    return angle

def angle_pic(angle, bs = (16,16)):
    radius = min(bs) // 2 - 1
    cy, cx = bs
    dx = radius * np.cos(angle)
    dy = radius * np.sin(angle)
    hog_image = np.zeros(bs, dtype=float)
    centre = tuple([cy // 2, cx // 2])
    rr, cc = draw.line(int(centre[0] - dx),
        int(centre[1] + dy),
        int(centre[0] + dx),
        int(centre[1] - dy))
    hog_image[rr, cc] += 1.
    return hog_image

def dftInitial(winw, winh):
    dft_M = cv2.getOptimalDFTSize(winw)
    dft_N = cv2.getOptimalDFTSize(winh)
    dft_A = np.zeros((dft_N, dft_M, 2), dtype=np.float64)
    return dft_M, dft_N, dft_A


if __name__ == '__main__':
    import sys
    import getopt

    print(__doc__)

    args, size = getopt.getopt(sys.argv[1:], '', 'shotdir=')
    size = str(size).strip('[]\'')
    args = dict(args)
    shotdir = args.get('--shotdir', '.')
    # If no specification, use the Maximum Resolution
    if len(size) == 0:
        size = '4224x3156'

#Prompt
    KidID = raw_input('KidID > ')
    w, h, cap = create_capture(size)

#cap.set(cv2.CAP_PROP_AUTOFOCUS, False)  # Known bug: https://github.com/Itseez/opencv/pull/5474
#cap.set(cv2.CAP_PROP_FOURCC, decode_fourcc())

cv2.namedWindow("KidPrint")

#convert_rgb = True
fps = int(cap.get(cv2.CAP_PROP_FPS))
#focus = int(min(cap.get(cv2.CAP_PROP_FOCUS) * 100, 2**31-1))  # ceil focus to C_LONG as Python3 int can go to +inf
fmethod = 0
#cv2.createTrackbar("Burst Count:", "KidPrint", burstCount, 20, lambda v: None)
cv2.createTrackbar("Focusing Method", "KidPrint", fmethod, 2, lambda v: None)
# Bri

'''
cv2.putText()
...
'''

Resol = "Resolution = " + str(w) + " x " + str(h)
# Select Specific part o f image for focus score
status, img = cap.read()
windowsize = [[int(w * (0.5 - focusWindow / 2)), int(w * (0.5 + focusWindow / 2))], [int(h * (0.5 - focusWindow / 2)), int(h * (0.5 + focusWindow / 2))]]

# Used for DTF function
winw = windowsize[0][1] - windowsize[0][0]
winh = windowsize[1][1] - windowsize[1][0]
dft_M, dft_N, dft_A = dftInitial(winw, winh)

# We want to calculate this value before the loop to determine the "Rectangle" Position
displayy = int(img.shape[0] * (displayx / img.shape[1]))
displaywindow = [[int(displayx * (0.5 - focusWindow / 2)), int(displayx * (0.5 + focusWindow / 2))], \
        [int(displayy * (0.5 - focusWindow / 2)), int(displayy * (0.5 + focusWindow / 2))]]

# Define some flags to be used by the infinite loop, used for indicating file name
K = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  #Representing number of images captured for each finger.
H = ['L', 'R']  #left or right hand?
indH = 0
Z = ['0', '1', '2', '3', '4'] #Representing five fingers accordingly
indZ = 0

# These flags are

# This is for counting the loop
i = 0
focus = False
his = False
fScore = 0

def shift_dft(src, dst=None):
    '''
        Rearrange the quadrants of Fourier image so that the origin is at
        the image center. Swaps quadrant 1 with 3, and 2 with 4.

        src and dst arrays must be equal size & type
    '''

    if dst is None:
        dst = np.empty(src.shape, src.dtype)
    elif src.shape != dst.shape:
        raise ValueError("src and dst must have equal sizes")
    elif src.dtype != dst.dtype:
        raise TypeError("src and dst must have equal types")

    if src is dst:
        ret = np.empty(src.shape, src.dtype)
    else:
        ret = dst

    h, w = src.shape[:2]

    cx1 = cx2 = w/2
    cy1 = cy2 = h/2

    # if the size is odd, then adjust the bottom/right quadrants
    if w % 2 != 0:
        cx2 += 1
    if h % 2 != 0:
        cy2 += 1

    # swap quadrants
    # swap q1 and q3
    ret[h-cy1:, w-cx1:] = src[0:cy1 , 0:cx1 ]   # q1 -> q3
    ret[0:cy2 , 0:cx2 ] = src[h-cy2:, w-cx2:]   # q3 -> q1

    # swap q2 and q4
    ret[0:cy2 , w-cx2:] = src[h-cy2:, 0:cx2 ]   # q2 -> q4
    ret[h-cy1:, 0:cx1 ] = src[0:cy1 , w-cx1:]   # q4 -> q2
    if src is dst:
        dst[:,:] = ret

    return dst


# Based on Opencv Sample Code dft.py
def dft(img, w = winw, h = winh):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    realInput = img.astype(np.float64)
    dft_A[:h, :w, 0] = realInput

    # no need to pad bottom part of dft_A with zeros because of
    # use of nonzeroRows parameter in cv2.dft()
    cv2.dft(dft_A, dst=dft_A, nonzeroRows = h)
    image_Re, image_Im = cv2.split(dft_A)

    # Compute the magnitude of the spectrum Mag = sqrt(Re^2 + Im^2)
    magnitude = cv2.sqrt(image_Re**2.0 + image_Im**2.0)

    # Compute log(1 + Mag)
    log_spectrum = cv2.log(1.0 + magnitude)

    # Rearrange the quadrants of Fourier image so that the origin is
    # at the image center
    shift_dft(log_spectrum, log_spectrum)

    # normalize and display the results as rgb
    cv2.normalize(log_spectrum, log_spectrum, 0.0, 1.0, cv2.NORM_MINMAX)
    cv2.imshow("magnitude", log_spectrum)


    # perform an optimally sized dft



while True:
    status, img = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    burstCount = cv2.getTrackbarPos("Burst Count:", "KidPrint")
    fn = '%s/%s_%s_%s_%02d.bmp' % (shotdir, KidID, H[indH], Z[indZ], K[indH][indZ])
    #brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)

    if his:
        # Histogram Display
        curve = hist_curve(img)
        cv2.imshow("Histogram", curve)

        # Focusing Score Calculation
    if fmethod == 1:
        fScore = rateFrame(img[windowsize[1][0]:windowsize[1][1],\
                windowsize[0][0]:windowsize[0][1]])
    elif fmethod == 2:
        pangle, fScore = patch_angle(img[windowsize[1][0]:windowsize[1][1],\
                windowsize[0][0]:windowsize[0][1]])
        angimage = angle_pic(pangle)
        cv2.imshow("Angle_Pic", angimage)
    elif fmethod == 3:
        dft(img[windowsize[1][0]:windowsize[1][1],\
                windowsize[0][0]:windowsize[0][1]])

    i += 1
    # These code is used to resize the output display to certain size
    img_new = cv2.resize(img, (int(displayx), displayy))

    cv2.putText(img_new, "FPS: {}".format(fps), (500, 40), font, 1.0, color)
    cv2.putText(img_new, Resol, (15, 40), font, 1.0, color)
    #cv2.putText(img_new, "Burst: {}".format(doBurst), (500, 40), font, 1.0, color)
    #cv2.putText(img_new, "Burst Count: {}".format(burstCount),(500, 80), font, 1.0, color)
    if fmethod == 1 or fmethod == 2 or fmethod == 3:
        cv2.putText(img_new, "Focus Score: {:.3f}".format(fScore),(500, 120), font, 1.0, color)
        cv2.putText(img_new, "Focus Method: {:d}".format(fmethod), (15, 120), font, 1.0, color)
        cv2.rectangle(img_new, (displaywindow[0][0], displaywindow[1][0]),\
                (displaywindow[0][1], displaywindow[1][1]), color, 1)

    cv2.putText(img_new, "File Name: {}".format(fn), (15, 80), font, 1.0, color)

    cv2.imshow("KidPrint", img_new)

    k = 0xFF & cv2.waitKey(1)

    if k == 27:
        break
    elif k == ord("h"):  #swich hands
        indH += 1
        if indH == 2:
            indH = 0
    elif k == ord("z"):
        indZ += 1
        if indZ == 5:
            indZ = 0
    elif k == ord(" "):
        cv2.imwrite(fn, img)
        print(fn, 'saved')
        K[indH][indZ] += 1
    elif k == ord("f"):
        fmethod += 1
        if fmethod == 4:
            fmethod = 0
    elif k == ord("b"):
        doBurst = not doBurst
    elif k == ord("w"):
        his = not his
cv2.destroyAllWindows()

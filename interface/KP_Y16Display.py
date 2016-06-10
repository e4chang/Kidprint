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
    i      - Histogram
    f      - focus score

    a,d    - Lens Value +-10
    w,s    - Lens Value +-1
    q,e    - lens value +-100
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np

import time     # Use to estimate FPS in real time

import KP_Serial as ks
import KP_impro as ki

#from skimage.filters import sobel_v, sobel_h
#from skimage import draw
#from skimage.exposure import equalize_hist

# Flags for indicating the state of the program
focus_control = False

# Define some flags to be used by the infinite loop, used for indicating file name
K = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]  #Representing number of images captured for each finger.
H = ['L', 'R']  #left or right hand?
indH = 0
Z = ['0', '1', '2', '3', '4'] #Representing five fingers accordingly
indZ = 0

displayx = 1024.0     # x-direction display resolution
focusWindow = 0.2     # relative size of focus window
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
burstCount = 1
lenval = 420        # Default Lens Value

# Some flags for controlling different function of the capturing
doBurst = False
focus = False
his = False
fScore = 0
fmethod = False

def create_capture(size = "3840x2160"):
    '''size=<value>
    '''

    size = str(size).strip()
    # Maybe we can set fourCC here

    cap = cv2.VideoCapture(1)
    w, h = map(int, size.split('x'))
    # The Size of the camera frames...
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    if cap is None or not cap.isOpened():
        print('Warning: unable to open video source: ', source)
    return w, h, cap


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

#cap.set(cv2.CAP_PROP_FOURCC, decode_fourcc())

cv2.namedWindow("KidPrint")

#convert_rgb = True
fps = int(cap.get(cv2.CAP_PROP_FPS))


Resol = "Resolution = " + str(w) + " x " + str(h)
# Select Specific part o f image for focus score
status, img = cap.read()
windowsize = [[int(w * (0.5 - focusWindow / 2)), int(w * (0.5 + focusWindow / 2))], [int(h * (0.5 - focusWindow / 2)), int(h * (0.5 + focusWindow / 2))]]

# We want to calculate this value before the loop to determine the "Rectangle" Position
displayy = int(img.shape[0] * (displayx / img.shape[1]))
displaywindow = [[int(displayx * (0.5 - focusWindow / 2)), int(displayx * (0.5 + focusWindow / 2))], \
       [int(displayy * (0.5 - focusWindow / 2)), int(displayy * (0.5 + focusWindow / 2))]]

# Initialize Serial Communication to ProMicro, also the lens, set lens value to 500
if focus_control:
    pm = ks.PMint()
    ks.lenint(pm)
    ks.lenset(pm, lenval)

# FPS Calculation
time_start = time.time()
frame_count = 0
fps = 0

# Image Acquiring Loop
while True:
    status, img = cap.read()

    # Determine the file name each time through Checking the Values of the
    fn = '%s/%s_%s_%s_%02d.bmp' % (shotdir, KidID, H[indH], Z[indZ], K[indH][indZ])

    if his:
        # Histogram Display
        curve = ki.hist_curve(img)
        cv2.imshow("Histogram", curve)

    img_new = cv2.resize(img, (int(displayx), displayy))

    cv2.putText(img_new, "FPS: {0:.2f}".format(fps), (500, 40), font, 1.0, color)
    cv2.putText(img_new, Resol, (15, 40), font, 1.0, color)
    cv2.putText(img_new, "File Name: {}".format(fn), (15, 80), font, 1.0, color)
    cv2.putText(img_new, "Lens Value: {}".format(lenval), (15, 120), font, 1.0, color)

    #cv2.putText(img_new, "Burst: {}".format(doBurst), (500, 40), font, 1.0, color)
    #cv2.putText(img_new, "Burst Count: {}".format(burstCount),(500, 80), font, 1.0, color)
    if fmethod:
        # Get a focus Score through canny edge detector
        fScore = ki.cannyRate(img[windowsize[1][0]:windowsize[1][1],\
                windowsize[0][0]:windowsize[0][1]])
        cv2.putText(img_new, "Focus Score: {:.3f}".format(fScore),(500, 120), font, 1.0, color)
        cv2.rectangle(img_new, (displaywindow[0][0], displaywindow[1][0]),\
                (displaywindow[0][1], displaywindow[1][1]), color, 1)


    cv2.imshow("KidPrint", img_new)

    # FPS Calculation
    frame_count += 1
    time_end = time.time()
    # Update Every two seconds
    if time_end > (time_start + 2):
        seconds = time_end - time_start
        fps = frame_count / seconds
        time_start = time.time()
        frame_count = 0


    # User key intepretation
    k = 0xFF & cv2.waitKey(1)

    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
    elif k == ord("h"):  #swich hands
        indH += 1
        if indH == 2:
            indH = 0
    elif k == ord("z"): # Switch Fingers
        indZ += 1
        if indZ == 5:
            indZ = 0
    elif k == ord(" "):	# Capture to destined directory
        cv2.imwrite(fn, img)
        print(fn, 'saved')
        K[indH][indZ] += 1
    elif k == ord("f"):
        fmethod = not fmethod
    elif k == ord("i"):
        his = not his
        if not his:
            cv2.destroyWindow("Histogram")
    elif (k == ord("s") and focus_control):
        lenval -= 1
        ks.lenset(pm, lenval)
    elif (k == ord("w") and focus_control):
        lenval += 1
        ks.lenset(pm, lenval)
    elif (k == ord("e") and focus_control):
        lenval += 100
        ks.lenset(pm, lenval)
    elif (k == ord("q") and focus_control):
        lenval -= 100
        ks.lenset(pm, lenval)
    elif (k == ord("a") and focus_control):
        lenval -= 5
        ks.lenset(pm, lenval)
    elif (k == ord("d") and focus_control):
        lenval += 5
        ks.lenset(pm, lenval)
    elif (k == ord("r") and focus_control):
        pm = ks.PMint()
        ks.lenint(pm)
        ks.lenset(pm, lenval)
cv2.destroyAllWindows()

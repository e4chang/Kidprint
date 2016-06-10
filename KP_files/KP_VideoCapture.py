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
from time import sleep
import numpy as np
import autofocus as af

import time     # Use to estimate FPS in real time

import KP_Serial as ks
import KP_impro as ki
import KP_tools as kt
import KP_capture as kc

#from skimage.filters import sobel_v, sobel_h
#from skimage import draw
#from skimage.exposure import equalize_hist


# Flags for indicating the state of the program
focus_control = True

# Some Parameter for image display
displayx = 1024.0     # x-direction display resolution
# Proportion of the focus window that we want to focus score calculation
focusWindow = 0.2

# Some flags for controlling different function of the capturing
doBurst = False
focus = False
his = False
fScore = 0
fmethod = False


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
        size = '1920x1080'

# Initialize the object
kid_ = kt.FileName(shotdir, raw_input('KidID > '), raw_input('Prototype Name >'))
cap_ = kc.capture()
dis_ = kc.display(cap_, kid_)

cv2.namedWindow("KidPrint")

# Select Specific part o f image for focus score
windowsize = [[int(cap_.w * (0.5 - cap_.focusWindow / 2)), \
        int(cap_.w * (0.5 + cap_.focusWindow / 2))], \
        [int(cap_.h * (0.5 - cap_.focusWindow / 2)), \
        int(cap_.h * (0.5 + cap_.focusWindow / 2))]]

# Initialize Serial Communication to ProMicro
#   , also the lens, set lens value to 'lenval'
if focus_control:
    pm_ = ks.PMint()
    ks.lenint(pm_)
    ks.lenset(pm_, 0)
else:
    pm_ = None

# FPS Calculation
time_start = time.time()
frame_count = 0

# Initialize keymapping object
key_ = kt.KeyMapping()

cnt = 0
state = af.FocusState()
lenval = 0
w = 0
h = 0

# Image Acquiring Loop
while True:
    cap_.readImg()
    dis_.displayImg()

    if his:
        # Histogram Display
        curve = ki.hist_curve(cap_.img)
        cv2.imshow("Histogram", curve)

    # Need to revise this part
    if fmethod:
        # Get a focus Score through canny edge detector
        fScore = ki.cannyRate(img[windowsize[1][0]:windowsize[1][1],\
                windowsize[0][0]:windowsize[0][1]])
        cv2.putText(img_new, "Focus Score: {:.3f}".format(fScore),\
                (500, 120), font, 1.0, color)
        cv2.rectangle(img_new, (displaywindow[0][0], displaywindow[1][0]),\
                (displaywindow[0][1], displaywindow[1][1]), color, 1)

    # FPS Calculation
    frame_count += 1
    time_end = time.time()

    # Update Every two seconds
    if time_end > (time_start + 2):
        seconds = time_end - time_start
        cap_.fps = frame_count / seconds
        time_start = time.time()
        frame_count = 0

    # Autofocus implementation with device
    if cnt > 0:
        cnt -= 1
        for i in range(5):
            cap_.readImg()
        img = cap_.img
        rating = af.rateFrame(img)
        delta = af.correctFocus(rating, state)
        print (rating)
        lenval += delta
        ks.lenset(pm_, lenval)
        if cnt == 0:
            lenval += state.stepToLastMax
            ks.lenset(pm_, lenval)
            cap_.w = w
            cap_.h = h
            cap_.updateRes()

    # User key intepretation
    k = 0xFF & cv2.waitKey(1)
    if k == ord("f"):
        cnt = 10
        state = af.FocusState()
        lenval = 0
        ks.lenset(pm_, lenval)
        w = cap_.w
        h = cap_.h
        cap_.w = 1280
        cap_.h = 720
        cap_.updateRes()

    e = key_.inputKey(cap_, kid_, k, focus_control, pm_)
    #e = kt.keyMapping(cap_, focus_control, kid_, pm, k)
    if e:
        break

cap_.release()
cv2.destroyAllWindows()



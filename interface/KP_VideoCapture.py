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
import KP_tools as kt
import KP_capture as kc
import KP_init

#from skimage.filters import sobel_v, sobel_h
#from skimage import draw
#from skimage.exposure import equalize_hist


# Flags for indicating the state of the program
focus_control = False

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
        from subprocess import check_output

        print(__doc__)

        args, size = getopt.getopt(sys.argv[1:], '', 'shotdir=')
        size = str(size).strip('[]\'')
        args = dict(args)
        shotdir = args.get('--shotdir', '.')
        # If no specification, use the Maximum Resolution
        if len(size) == 0:
            size = '1920x1080'

        # Prompting for user inputs
        app = 'v4l2-ctl'
        inq = '--list-devices'
        dev_pre = '-d'
        print('Available Video Devices:')
        buf = check_output([app, inq]) # List all the avaliable devices
        print(buf)
        dl = raw_input('Use: Video')

# Contain All the initilization function
(kid_, cap_, dis_) = KP_init.init(shotdir, dl)
key_ = KP_init.init_key()

if(focus_control == True):
    pm_ = init_focus()
else:
    pm_ = None

# FPS Calculation
time_start = time.time()
frame_count = 0

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
        fScore = ki.cannyRate(img[cap_.fwindowsize[1][0]:\
                cap_.fwindowsize[1][1],\
                cap_.fwindowsize[0][0]:\
                cap_. fwindowsize[0][1]])
        cv2.putText(img_new, "Focus Score: {:.3f}".format(fScore),\
                (500, 120), font, 1.0, color)
        cv2.rectangle(img_new, (displaywindow[0][0], displaywindow[1][0]),\
                (displaywindow[0][1], displaywindow[1][1]), color, 1)

    # FPS Calculation
    frame_count += 1
    time_end = time.time()

    # Update Every two seconds, FPS and Exposure
    if time_end > (time_start + 2):
        seconds = time_end - time_start
        cap_.fps = frame_count / seconds
        time_start = time.time()
        frame_count = 0
        # Quick and Dirty Function for updating the filename
        cap_.updateExp()
        kid_.updateExp(cap_.exp)
        kid_.updateFn()

    # User key intepretation
    k = 0xFF & cv2.waitKey(1)
    e = key_.inputKey(cap_, kid_, k, focus_control, pm_)
    #e = kt.keyMapping(cap_, focus_control, kid_, pm, k)
    if e:
        break

cap_.release()
cv2.destroyAllWindows()

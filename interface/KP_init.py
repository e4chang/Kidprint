import cv2

import KP_tools as kt
import KP_capture as kc
import KP_Serial as ks

def init(shotdir = '.', dl = 0):
    # Initialize the object
    kid_ = kt.FileName(shotdir, raw_input('KidID > '), \
            raw_input('Prototype Name > '))
    cap_ = kc.capture(dl)
    dis_ = kc.display(cap_, kid_)
    cv2.namedWindow("Kidprint")
    return (kid_, cap_, dis_)


# Select Specific part o f image for focus score
def init_focus():
# Initialize Serial Communication to ProMicro
#   , also the lens, set lens value to 'lenval'
    pm_ = ks.PMint()
    ks.lenint(pm_)
    ks.lenset(pm_, 420)
    return pm_

def init_key():
# Initialize keymapping object
    key_ = kt.KeyMapping()
    return key_


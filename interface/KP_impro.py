import cv2
import numpy as np

# Show the histogram of the image
def hist_curve(im):
    bins = np.arange(256).reshape(256, 1)
    h = np.zeros((300,256,3))
    logs = np.zeros((256, 3))
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
def cannyRate(img):
    s = 0
    size = img.shape[1] * img.shape[0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)
    #cv2.imshow("Gaussian", img)
    img = cv2.Canny(img, 0, 30, 3)
    cv2.imshow("Canny", img)
    s = np.sum(img)
    return s / float(size)


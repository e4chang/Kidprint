import cv2
import numpy as np
from subprocess import check_output

# There are two purpose for this class--> Input Video and Display
class capture:
    def __init__(self, dl = "0", size = "3840x2160"):
        self.size = str(size).strip()
        self.cap = cv2.VideoCapture(int(dl))
        self._w, self._h = map(int, size.split('x'))
        self._focusWindow = 0.2     # relative size of focus window
        self._dl = dl
        # The Size of the camera frames...
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._h)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._w)
        self.exp = self.updateExp()

        self.fwindowsize = [[int(self._w * (0.5 - self._focusWindow / 2)), \
                            int(self._w * (0.5 + self._focusWindow / 2))], \
                            [int(self._h * (0.5 - self._focusWindow / 2)), \
                            int(self._h * (0.5 + self._focusWindow / 2))]]

        if self.cap is None or not self.cap.isOpened():
            print('Warning: unable to open video source: ', dl)

        self.status, self.img = self.cap.read()
        self.fps = 0.0

    def readImg(self):
        self.status, self.img = self.cap.read()

    def release(self):
        self.cap.release()

    def updateExp(self):
        app = 'v4l2-ctl'
        dev_pre = '-d'
        ckvar = '-C'
        expcommand = 'exposure_absolute'
        buf = check_output([app, dev_pre, self._dl, ckvar, expcommand])
        [name, value] = buf.split(":")
        self.exp = value.strip()

class display:
    def __init__(self, capture, kid):
        self.displayx = 1024.0
        self.displayy = int(capture.img.shape[0] * (self.displayx / capture.img.shape[1]))
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.color = (0, 255, 0)
        self.cap_ = capture
        self.kid_ = kid
        # We want to calculate this value before the loop to determine the "Rectangle" Position
        self.displaywindow = [[int(self.displayx * (0.5 - self.cap_._focusWindow / 2)), \
                int(self.displayx * (0.5 + self.cap_._focusWindow / 2))], \
                [int(self.displayy * (0.5 - self.cap_._focusWindow / 2)), \
                int(self.displayy * (0.5 + self.cap_._focusWindow / 2))]]

    def displayImg(self):
        self.displayimg = cv2.resize(self.cap_.img, (int(self.displayx), self.displayy))
        cv2.putText(self.displayimg, "FPS: {0:.2f}".\
                format(self.cap_.fps), (500, 40), self.font, 1.0, \
                self.color)
        cv2.putText(self.displayimg, "Resolution = {}x{}".\
                format(self.cap_._w, self.cap_._h), (15, 40), \
                self.font, 1.0, self.color)
        cv2.putText(self.displayimg, "File Name: {}".\
                format(self.kid_.fn), (15, 80), self.font, 1.0, \
                self.color)
        #cv2.putText(self.displayimg, "Lens Value: {}".format(lenval), (15, 120), self.font, 1.0, self.color)
       # cv2.putText(self.displayimg, "Exposure(absolute): {}".format(expo), (500, 80), font, 1.0, color)
        cv2.imshow("Kidprint", self.displayimg)

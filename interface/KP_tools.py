import cv2
import os
import re
from datetime import date
import KP_Serial as ks


# Dealing with all the file namings
class FileName:
    # Representing number of images captured for each finger in current
    # Directory
    _K = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    # These are constants and should not be changed
    _H = ['L', 'R']                 #left or right hand?
    _Z = ['0', '1', '2', '3', '4']  #Representing five fingers accordingly

    def __init__(self, directory = './', kidID = 'KP000', proto = '000'):
        self.indH = 0
        self.indZ = 0
        # Define some flags to be used by the infinite loop,
        # used for indicating file name
        self._fileindex = FileIndex(directory)
        self._directory = directory
        self._kidID = kidID
        self._proto = proto
        self._ext = '.bmp'
        self._delim = '_'
        self._exp = 100
        self.refreshFolder(directory)
        self.updateFn()

    # This can be used in case we want to change folders or refresh the index
    def refreshFolder(self, directory):
        self._fileindex.directory = directory
        self._fileindex.readFiles(self._kidID)
        for i in range(2):
            for k in range(5):
                #abc = self._fileindex.getSequence(i,k)
                self._K[i][k] = self._fileindex.getSequence(i,k)

    # FileName needs to be updated when ever the parameters are changed
    # FileName Standard,
    # 'ID_HAND_FINGER_SEQUENCE_PROTOTYPE_EXPOSURE_RESOLUTION'
    def updateFn(self):
      mydate = date.today().strftime("%m-%d-%y")
      self.fn = '%s/%s_%s_%s_%s_%03d' % (self._directory, self._kidID, \
              mydate, self._H[self.indH], self._Z[self.indZ], \
              self._K[self.indH][self.indZ])
      self.fn = self.fn + self._delim + self._proto
      self.fn = self.fn + self._delim + str(self._exp) + self._ext

    def updateInd(self, delta):
        # Can change index in any way
        self._K[self.indH][self.indZ] += delta
    def updateKidID(self, kidID):
        self._kidID = kidID
    def updateExp(self, exp):
        self._exp = exp

# The class will read the file name in arbitrary directory and output the
# sequence number for each finger under specific KidID
class FileIndex():

    def __init__(self, directory = './'):
        # This directory can be updated at run time to load current value
        self.directory = './'
        self._delim = '_'
        self._ext = '.bmp'
        # Add '_.*.' So that additional attributions may be added in the future
        self._fileRegex = r'_\d{2}-\d{2}-(\d{2}|\d{4})_[LR]_[0-4]_\d{3}.*\.bmp$'
        self._Hindex = 2 # L or R
        self._Findex = 3 # 0-4
        self._Sindex = 4 # 00-99
        self._nextSequence = [[0 for i in range(5)] for j in range(2)]

    # Reads all files in directory and fills next sequence values
    def readFiles(self, kpid):

        regex = '^' + kpid + self._fileRegex
        files = os.listdir(self.directory)
        p = re.compile(regex)
        matches = []
        for f in files:
            if p.match(f):
                matches.append(f)

        for match in matches:
            m = match.strip(self._ext)
            finger = m.split(self._delim)
            H = self._hand(finger[self._Hindex])
            F = int(finger[self._Findex])
            S = int(finger[self._Sindex])

            curr = self._nextSequence[H][F]
            self._nextSequence[H][F] = S+1 if S >= curr else curr

    # Inputs:
    #   H: 0 or 1 --> 'L' or 'R'
    #   F: 0-4
    def getSequence(self, H, F):
        return self._nextSequence[int(H)][int(F)]

    def _hand(self, h): return 0 if h == 'L' or h == 0 else 1

class KeyMapping():

    def __init__(self):
        self._lenval = 420


    def inputKey(self, cap_, kid, k = 0, focus_control = False, pm = None):
        lenval = self._lenval
        if k == 27:
            return 1
        elif k == ord("h"):  #swich hands
            kid.indH += 1
            if kid.indH == 2:
                kid.indH = 0
            kid.updateFn()
        elif k == ord("z"): # Switch Fingers
            kid.indZ += 1
            if kid.indZ == 5:
                kid.indZ = 0
            kid.updateFn()
        elif k == ord(" "):	# Capture to destined directory
            cv2.imwrite(kid.fn, cap_.img)
            print(kid.fn, 'saved')
            # Abstract them into one function
            kid.updateInd(1)
            kid.updateFn()
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
        self._lenval = lenval
        return 0

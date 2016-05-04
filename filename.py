import os
import re

delim = '_'
ext = '.bmp'
directory = '.'
fileRegex = 'KP\d{3}_[LR]_[0-4]_\d{2}\.bmp'
Hindex = 1 # L or R
Findex = 2 # 0-4
Sindex = 3 # 00-99

nextSequence = [[0 for i in range(5)] for j in range(2)]

def hand(h): return 0 if h == 'L' or h == 0 else 1

# Reads all files in directory and fills next sequence values
def readFiles():

    files = os.listdir(directory)
    p = re.compile(fileRegex)
    matches = []
    for f in files:
        if p.match(f):
            matches.append(f)

    #print matches
    #print nextSequence

    for match in matches:
        m = match.strip(ext)
        finger = m.split(delim)
        H = hand(finger[Hindex])
        F = int(finger[Findex])
        S = int(finger[Sindex])

        curr = nextSequence[H][F]
        nextSequence[H][F] = S+1 if S >= curr else curr
    #print nextSequence

# Inputs:
#   H: 'L' or 'R'
#   F: 0-4
def getSequence(H,F):
    H = hand(H)
    F = int(F)
    return nextSequence[H][F]

readFiles()
print 'Left 4:', getSequence('L', 4)

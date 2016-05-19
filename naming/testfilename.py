import os
import re

fileDelim = '_'
fileExt   = '.bmp'

def getFilename(params):
    f = ''.join('%s_' % p for p in params).strip('_') + fileExt
    return f

kidprint = ['kp01', '0', '1', '12']
getFilename(kidprint)

directory = '.'
fileRegex = 'asdf_[LR]_[0-4]_\d{2}\.bmp'
Hindex = Filename.HAND.value
Findex = Filename.FINGER.value
Sindex = Filename.SEQUENCE.value

def readFiles():

    files = os.listdir(directory)
    p = re.compile(fileRegex)
    matches = []
    for f in files:
        if p.match(f):
            print 'Matched:', f
            matches.append(f)

    indices = [[0 for i in range(5)] for j in range(2)]
    print indices
    def hand(h): return 0 if h == 'L' else 1
    for match in matches:
        m = match.split('.')[0]
        finger = m.split('_')
        H = hand(finger[Hindex])
        F = int(finger[Findex])
        S = int(finger[Sindex])

        curr = indices[H][F]
        indices[H][F] = S+1 if S >= curr else curr
    print indices

readFiles()


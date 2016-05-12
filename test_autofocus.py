import autofocus
import math
import random
import matplotlib.pyplot as plt
from scipy import signal

NOISE = 0.02
MAX_FOCUS = 1024
ITERATIONS = 12
def noise():
    return NOISE - random.random() * 2 * NOISE

# Generate half period noisy sine wave
def generateSineWave(offset):
	HALF = MAX_FOCUS / 2
	offset = HALF if offset > HALF else -HALF if offset < -HALF else offset
	return [math.sin(math.pi*(i-offset)/MAX_FOCUS) + noise() for i in range(MAX_FOCUS)]

def testAutofocus():
    focusPoint = 0
    state = autofocus.FocusState()
    # function = generateSineWave(300)
    # generate gaussian function centered ~300
    gauss = signal.gaussian(624, std=50)
    function = [0 for i in range(1024)]
    for g in range(len(gauss)):
        function[g] = gauss[g] + noise()
    foci = [0,0]
    for i in range(ITERATIONS):
        state.lastSucceeded = focusPoint < len(function) and focusPoint >= 0
        stepVal = autofocus.correctFocus(function[int(focusPoint)], state)
        focusPoint = focusPoint + stepVal
        focusPoint = 0 if focusPoint < 0 else focusPoint
        focusPoint = len(function)-1 if focusPoint >= len(function) else focusPoint
        foci.append(int(focusPoint))

    fociVal = []
    for f in foci:
        fociVal.append(function[f])

    plt.plot(function, 'r.', foci, fociVal, 'b^', focusPoint+state.stepToLastMax , state.rateMax, 'gs')
    plt.xlabel('Lens distance')
    plt.ylabel('Focus rating')
    plt.show()
#state = autofocus.FocusState()
testAutofocus()


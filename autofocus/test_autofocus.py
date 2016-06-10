# Driver script to test the autofocus modules

import autofocus
import math
import random
import time
import matplotlib.pyplot as plt
from scipy import signal

# Constants
NOISE = 0.01
MAX_FOCUS = 1024
ITERATIONS = 20

# Random value used to distort a point
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
    gauss = signal.gaussian(624, std=50)      # Generate Gaussian function
    function = [0 for i in range(1024)]
    for g in range(len(gauss)):               # Distort the Gaussian func
        function[g] = gauss[g] + noise()
    foci = [0,0]

    print function

    # Test the function for getting next focus value and plot it
    for i in range(ITERATIONS):
        state.lastSucceeded = focusPoint < len(function) and focusPoint >= 0
        stepVal = autofocus.correctFocus(function[int(focusPoint)], state)
        focusPoint = focusPoint + stepVal
        focusPoint = 0 if focusPoint < 0 else focusPoint
        focusPoint = len(function)-1 if focusPoint >= len(function) else focusPoint
        foci.append(int(focusPoint))
        plt.plot( focusPoint, function[focusPoint], 'b^')
        print focusPoint, function[focusPoint], 'b^'

    #fociVal = []
    #for f in foci:
    #    fociVal.append(function[f])

    plt.plot( focusPoint+state.stepToLastMax , state.rateMax, 'gs')
    print focusPoint + state.stepToLastMax, state.rateMax

def testAutofocusGui():
    focusPoint = 0
    state = autofocus.FocusState()
    # function = generateSineWave(300)
    gauss = signal.gaussian(624, std=50)      # Generate Gaussian function
    function = [0 for i in range(1024)]
    for g in range(len(gauss)):               # Distort the Gaussian func
        function[g] = gauss[g] + noise()
    foci = [0,0]

    # Plot the points of the simulated function
    plt.plot(function, 'r.')
    plt.ion()
    plt.pause(5)

    # Test the function for getting next focus value and plot it
    for i in range(ITERATIONS):
        state.lastSucceeded = focusPoint < len(function) and focusPoint >= 0
        stepVal = autofocus.correctFocus(function[int(focusPoint)], state)
        focusPoint = focusPoint + stepVal
        focusPoint = 0 if focusPoint < 0 else focusPoint
        focusPoint = len(function)-1 if focusPoint >= len(function) else focusPoint
        foci.append(int(focusPoint))
        plt.plot( focusPoint, function[focusPoint], 'b^')
        plt.pause(0.5)

    #fociVal = []
    #for f in foci:
    #    fociVal.append(function[f])

    # Plot the maximum focus point found
    plt.plot( focusPoint+state.stepToLastMax , state.rateMax, 'gs')
    plt.xlabel('Lens distance')
    plt.ylabel('Focus rating')
    #plt.show()
    while True:
        plt.pause(0.05)
#state = autofocus.FocusState()
testAutofocus()


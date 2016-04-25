import autofocus
import math
import random

NOISE = 0.005
MAX_FOCUS = 1024

def noise():
    return NOISE - random.random() * 2 * NOISE

def generateWave(offset):
	HALF = MAX_FOCUS / 2
	offset = HALF if offset > HALF else -HALF if offset < -HALF else offset
	return [math.sin(math.pi*(i-offset)/MAX_FOCUS) + noise() for i in range(MAX_FOCUS)]

def testAutofocus():
    global lastSucceeded
    focusPoint = 0
    state = autofocus.FocusState()
    sinFunc = generateWave(200)
    for i in range(20):
        lastSucceeded = focusPoint < len(sinFunc) and focusPoint >= 0
        stepVal = autofocus.correctFocus(sinFunc[int(focusPoint)], state)
        print int(stepVal), sinFunc[int(focusPoint)], '\n'
        focusPoint = focusPoint + stepVal
        focusPoint = 0 if focusPoint < 0 else focusPoint
        focusPoint = len(sinFunc)-1 if focusPoint >= len(sinFunc) else focusPoint
        print state.stepToLastMax, focusPoint

#state = autofocus.FocusState()
#print state.direction
#print autofocus.correctFocus(0.0)
testAutofocus()


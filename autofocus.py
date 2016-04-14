
# coding: utf-8

# In[22]:

# previous state
prevFocus = 0
step = 0
direction = 0
iterationRates = []

# constants
epsylon = 0.05
MAX_FOCUS = 1024
STEPS_PER_CYCLE = 4

def initialize():
    global prevFocus
    global direction
    global step
    prevFocus = 0
    direction = 1
    step = MAX_FOCUS / 4


# using binary search to find focal point
# assumes initial focus at point 0
# [ | |^| ]
def autofocus(rate):
    global step, prevFocus
    nextFocus = step + prevFocus
    if direction == 1 and nextFocus < MAX_FOCUS:
        # find the quadrant with the maximum surrounding rates
        iterationRates.append(rate)
        prevRate = rate
        deltaRate = rate - prevRate
        prevFocus = nextFocus
        return step
    elif direction == 1:
        for i in range(len(iterationRates)):
            if iterationRates > 
    elif direction == -1:
        step = step / 4
            
    # TODO: set direction = 0 when rate doesn't change after 3 iterations
    elif direction == 0:
        # midpoint
        step = step
    return 0


# In[24]:

initialize()
print(autofocus(87.5))
print(autofocus(88.5))
print(autofocus(89.5))
print(autofocus(91.5))


# In[49]:

import math
import random
NOISE = 0.02

def noise():
    return NOISE - random.random() * 2 * NOISE

def generateWave():
    wave = [math.sin(math.pi*i/MAX_FOCUS) + noise() for i in range(MAX_FOCUS)]

def testAutofocus():
    focusPoint = 0
    sinFunc = generateWave()
    for i in range(20):
        stepVal = autofocus(sinFunc[focusPoint])
        focusPoint = focusPoint + stepVal


# In[ ]:




# In[ ]:




FOCUS_STEP = 128                    # Initial step value
epsylon = 0.001                     # Threshold value
class FocusState:

  # Initialize state - used to keep track of previous focus
	def __init__(self):
	    self.direction = 1
	    self.step = FOCUS_STEP
	    self.stepToLastMax = 0
	    self.rate = 0.0
	    self.rateMax = 0.0
	    self.lastSucceeded = True
	    self.minFocusStep = 2
	    self.lastDirectionChange = 0

# This function calculates the next step to change focus
def correctFocus(rate, state):
	state.lastDirectionChange += 1
	rateDelta = rate - state.rate

  # Found new maximum
	if rate > state.rateMax + epsylon:
		state.stepToLastMax = 0
		state.rateMax = rate
		lastDirectionChange = 0

  # Last state went out of bounds
	if not state.lastSucceeded:
		state.direction *= -1
		state.lastDirectionChange = 0
		state.step = state.step / 2

  # Last state was successful
	else:
    # No change
		if rate < epsylon:
			state.step = FOCUS_STEP
    # Wrong direction
		elif rateDelta < -epsylon:
			state.direction *= -1
			state.step = state.step * 3 / 4
			state.lastDirectionChange = 0
    # Did not increase focus for 3 steps or min step reached
		elif ((rate + epsylon < state.rateMax) and
		     ((state.lastDirectionChange > 3) or
         (state.step < (state.minFocusStep * 3 / 2) and
         state.stepToLastMax > state.step))):
			state.direction = 1 if state.stepToLastMax >= 0 else -1
			state.step = state.step * 3 / 4
			stepToMax = state.stepToLastMax
			state.stepToLastMax = 0
			state.lastDirectionChange = 0
			state.rate = rate
			return stepToMax

  # Calculate and return new step value
	state.rate = rate
	tempStep = state.direction * state.step
	state.stepToLastMax -= tempStep
	return tempStep

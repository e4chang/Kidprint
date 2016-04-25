FOCUS_STEP = 256
epsylon = 0.001
class FocusState:

	def __init__(self):
	    self.direction = 1
	    self.step = FOCUS_STEP
	    self.stepToLastMax = 0
	    self.rate = 0.0
	    self.rateMax = 0.0
	    self.lastSucceeded = True
	    self.minFocusStep = 1
	    self.lastDirectionChange = 0

#state = FocusState()
#print state.direction

def correctFocus(rate, state):
	# print state.direction
	state.lastDirectionChange += 1
	rateDelta = rate - state.rate

	if rate > state.rateMax + epsylon:
		state.stepToLastMax = 0
		state.rateMax = rate
		lastDirectionChange = 0

	if not state.lastSucceeded:
		state.direction *= -1
		state.lastDirectionChange = 0
		state.step = state.step / 2
	else:
		if rate < epsylon:
			state.step = FOCUS_STEP
		elif rateDelta < -epsylon:
			state.direction *= -1
			state.step = state.step * 0.75
			state.lastDirectionChange = 0
		elif (rate + epsylon < state.rateMax) and (state.lastDirectionChange > 3) or (state.step < (state.minFocusStep * 1.5) and state.stepToLastMax > state.step):
			state.direction = 1 if state.stepToLastMax >= 1 else -1
			state.step = state.step * 0.75
			stepToMax = state.stepToLastMax
			state.stepToLastMax = 0
			state.lastDirectionChange = 0
			state.rate = rate
			#print 2
			return stepToMax
	#print lastDirectionChange
	state.rate = rate
	state.step = state.direction * state.step
	state.stepToLastMax -= state.step
	return state.step
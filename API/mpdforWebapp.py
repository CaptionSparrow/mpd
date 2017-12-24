import random as rnd
import numpy as np
from copy import deepcopy

# Define the utility matrix here
U = [[[2,-1],[3,0]],[[2,3],[-1,0]]]  # The matrix is 2 by 2 by 2

# Define the game scality here
N = 12  # Initial number of players
P = [0.0, 0.5, 1.0]  # Initial strategies of players
R = 80   # The rounds played
M = 5  # The number of games played in each round
T = ["TFT", "Random"] # The types contained in the game
PT = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # The proportion of the types

Types = ["Constant", "Random", "Action_based", "TFT", "Co_TFT", "Revenger", "Krevenger", "RKrevenger", "Bayesian"]

# Parameters
# For Action_based
Ka = 0.02
# For Co_TFT
Kc = 2
# For Krevenger
Kr = 2
# For RKrenvenger
Krb = 2
Krc = 2

# For Bayesian
Kb = 5

def p11(history, myhistory):
	if history[0] < Kb:
		return 1
	else:
		p = CoopCoop_times(history, myhistory)
		if p == inf:
			return 1
		else:
			return p

def p12(history, myhistory):
	if history[0] < Kb:
		return 0
	else:
		p = CoopBetray_times(history, myhistory)
		if p == inf:
			return 1
		else:
			return p

def p21(history, myhistory):
	if history[0] < Kb:
		return 1
	else:
		p = BetrayCoop_times(history, myhistory)
		if p == inf:
			return 1
		else:
			return p

def p22(history, myhistory):
	if history[0] < Kb:
		return 0
	else:
		p = BetrayBetray_times(history, myhistory)
		if p == inf:
			return 1
		else:
			return p

# Some useful functions
def cBetray_times(history):
	times = 0
	for i in range(history[0] + 1, 2, -1):
		if history[i] == 1:
			times += 1
		else:
			break
	return times

def cCoop_times(history):
	times = 0
	for i in range(history[0] + 1, 2, -1):
		if history[i] == 0:
			times += 1
		else:
			break
	return times

# Some useful functions
def cBetray_times(history):
	times = 0
	for i in range(history[0] + 1, 2, -1):
		if history[i] == 1:
			times += 1
		else:
			break
	return times

def cCoop_times(history):
	times = 0
	for i in range(history[0] + 1, 2, -1):
		if history[i] == 0:
			times += 1
		else:
			break
	return times

def BetrayBetray_times(history, myhistory):
	if myhistory[1] == 0:
		return inf
	else:
		m = 0
		n = 0
		for i in range(2, history[0] + 1):
			if myhistory[i] == 1:
				n += 1
				if history[i] == 1:
					m += 1
		return m / n

def CoopBetray_times(history, myhistory):
	if myhistory[1] == 0:
		return inf
	else:
		return 1 - BetrayBetray_times(history, myhistory)

def BetrayCoop_times(history, myhistory):
	if myhistory[0] == myhistory[1]:
		return inf
	else:
		m = 0
		n = 0
		for i in range(2, history[0] + 1):
			if myhistory[i] == 0:
				n += 1
				if history[i] == 1:
					m += 1
		return m / n

def CoopCoop_times(history, myhistory):
	if myhistory[0] == myhistory[1]:
		return inf
	else:
		return 1 - BetrayCoop_times(history, myhistory)

class player:
	def __init__(self):
		self._strategy = P[1]      # The player can distinguish each other in the base model so the strategies stored in a dictionary
		self._points = 0         # The initial score of the player is 0
		t = rnd.randint(0,8)
		self._type = Types[t]

		self._history = [0,0]       # The playing history of the players

		#--For Bayesian Type--#
		self._matrix = np.matrix([[1., 0.], [0., 1.]])
		#---------------------#

	def getType(self):
		return self._type

	def strategy(self):
		return self._strategy

	#----------------To be implenmented----------------#
	def modify_strategy(self, my_action, ad_action):
		if self.getType() == "Constant":
			pass
		elif self.getType() == "Random":
			new_strategy = rnd.random()
			self._strategy = new_strategy
		elif self.getType() == "Action_based":
			if ad_action == 0:
				self._strategy = min(self._strategy + Ka * self.points(), 1.)
			else:
				self._strategy = max(self._strategy - Ka * self.points(), 0.)
		elif self.getType() == "TFT":
			if ad_action == 0:
				self._strategy = 1.
			else:
				self._strategy = 0.
		elif self.getType() == "Co_TFT":
			if ad_action == 0:
				self._strategy = 1.
			else:
				if cBetray_times(self._history) > Kc:
					self._strategy = 0.
				else:
					self._strategy = 1.
		elif self.getType() == "Revenger":
			if ad_action == 1:
				self._strategy = 0.
		elif self.getType() == "Krevenger":
			if cBetray_times(self._history) > Kr:
				self._strategy = 0.
		elif self.getType() == "RKrevenger":
			if cBetray_times(self._history) > Krb:
				self._strategy = 0.
			elif cCoop_times(self._history) > Krc:
				self._strategy = 1.
		elif self.getType() == "Bayesian":
			self._matrix[0, 0] = p11(self._history, self._myhistory)
			self._matrix[0, 1] = p12(self._history, self._myhistory)
			self._matrix[1, 0] = p21(self._history, self._myhistory)
			self._matrix[1, 1] = p22(self._history, self._myhistory)
			old_p = np.matrix([[self.strategy()], [1 - self.strategy()]])
			new_p = np.dot(self._matrix, old_p)
			self._strategy = new_p[0, 0]
	#----------------To be implenmented----------------#

	def points(self):
		return self._points

	def add_points(self, u):
		self._points += u

	def playwith(self, ad_action):
		action = rnd.random()

		if action <= self.strategy():
			act = 0                     # 0 means cooperation
		else:
			act = 1                     # 1 means betrayal

		self.update_history(ad_action, act)
		self.modify_strategy(act,ad_action)

		d_u = U[0][act][ad_action]
		d_au = U[1][act][ad_action]

		self.add_points(d_u)

		return (act, d_u, d_au)

	def update_history(self, ad_action, my_action):
		self._history[0] += 1			# Playing times add 1
		self._history[1] += ad_action	# Times betrayal add 1
		self._history.append(ad_action)
		self._myhistory[0] += 1			# Playing times add 1
		self._myhistory[1] += my_action	# Times betrayal add 1
		self._myhistory.append(my_action)
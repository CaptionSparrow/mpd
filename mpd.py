import random as rnd
import numpy as np
from copy import deepcopy
from math import inf

#-----------------Parameters modified here-----------------#
# Define the utility matrix here
U = [[[2,-1],[3,0]],[[2,3],[-1,0]]]  # The matrix is 2 by 2 by 2

# Define the game scality here
N = 12  # Initial number of players
P = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Initial strategies of players
R = 80   # The rounds played
M = 5  # The number of games played in each round
T = ["Bayesian", "Const"] # The types contained in the game
folder_name = "BayesianvsConst_12_5_80" # Folder name
PT = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] # The proportion of the types

# Define Types
#----------------------------------------------------------#
# Non-memory
'''
Constant:		never change his/her strategy, the inital strategy
        		will indicate the concrete type of the person;
Random:			change his/ her strategy randomly;
Action_based:	change the strategy based on the current point;
'''

# Memory
'''
TFT:			tit for tat
Co_TFT:			co-tft
Revenger:		revenge if one cheats
Krevenger:		revenge if one cheats k times
RKrevenger:		may recover after some times not cheating
Bayesian:		step update based on probability
'''

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
#----------------------------------------------------------#

# Write data in file with json format
#----------------------------------------------------------#
def wdata_points(data, num, pr):
	f = open("data\\"+folder_name+"\\points_"+str(pr)+"_"+str(num+1)+".json", 'w')
	n = len(data)
	m = len(data[0])
	print("{", file=f)

	print('  "ID":[', end="", file=f)
	for i in range(n-1):
		print('"'+str(i)+'"', end=",", file=f)
	print('"'+str(n-1)+'"],', file=f)

	for i in range(m-1):
		print('  "ROUND'+str(i+1)+'":[', end="", file=f)
		for j in range(n-1):
			print('"'+str(data[j][i])+'"', end=",", file=f)
		print('"'+str(data[n-1][i])+'"],', file=f)

	print('  "ROUND'+str(m)+'":[', end="", file=f)
	for j in range(n-1):
		print('"'+str(data[j][m-1])+'"', end=",", file=f)
	print('"'+str(data[n-1][m-1])+'"]', file=f)

	print("}", file=f)

	f.close()

	#------------------------------------#

	f = open("data\\"+folder_name+"\\pointsp_"+str(pr)+"_"+str(num+1)+".json", 'w')
	print("{", file=f)

	print('  "Points":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print(str(data[i][j]), end=",", file=f)
	for i in range(m-1):
		print(str(data[n-1][i]), end=",", file=f)
	print(str(data[n-1][m-1])+'],', file=f)

	print('  "Round":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print(str(j+1), end=",", file=f)
	for i in range(m-1):
		print(str(i+1), end=",", file=f)
	print(str(m)+'],', file=f)

	print('  "categ":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print('"player'+str(i)+'"', end=",", file=f)
	for i in range(m-1):
		print('"player'+str(n-1)+'"', end=",", file=f)
	print('"player'+str(n-1)+'"]', file=f)

	print("}", file=f)

	f.close()

def wdata_actions(data, num, pr):
	f = open("data\\"+folder_name+"\\actions_"+str(pr)+"_"+str(num+1)+".json", 'w')
	n = len(data)
	m = len(data[0])
	print("{", file=f)

	print('  "ID":[', end="", file=f)
	for i in range(n-1):
		print('"'+str(i)+'"', end=",", file=f)
	print('"'+str(n-1)+'"],', file=f)

	for i in range(m-1):
		print('  "ROUND'+str(i+1)+'":[', end="", file=f)
		for j in range(n-1):
			print('"'+str(data[j][i])+'"', end=",", file=f)
		print('"'+str(data[n-1][i])+'"],', file=f)

	print('  "ROUND'+str(m)+'":[', end="", file=f)
	for j in range(n-1):
		print('"'+str(data[j][m-1])+'"', end=",", file=f)
	print('"'+str(data[n-1][m-1])+'"]', file=f)

	print("}", file=f)

	f.close()

		#------------------------------------#

	f = open("data\\"+folder_name+"\\actionsp_"+str(pr)+"_"+str(num+1)+".json", 'w')
	print("{", file=f)

	print('  "Data":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print(str(data[i][j]), end=",", file=f)
	for i in range(m-1):
		print(str(data[n-1][i]), end=",", file=f)
	print(str(data[n-1][m-1])+'],', file=f)

	print('  "x.label":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print('"ROUND'+str(j+1)+'"', end=",", file=f)
	for i in range(m-1):
		print('"ROUND'+str(i+1)+'"', end=",", file=f)
	print('"ROUND'+str(m)+'"],', file=f)

	print('  "categ":[', end="", file=f)
	for i in range(n-1):
		for j in range(m):
			print('"player'+str(i)+'"', end=",", file=f)
	for i in range(m-1):
		print('"player'+str(n-1)+'"', end=",", file=f)
	print('"player'+str(n-1)+'"]', file=f)

	print("}", file=f)

	f.close()
#----------------------------------------------------------#

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
		for i in range(2, history[0] + 2):
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
		for i in range(2, history[0] + 2):
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

#-------------------Classes defined here-------------------#
# Class for the each player
class player:
	def __init__(self, idex, p0, Type):
		self._id = idex          # The index of the player, which will be set at the initial
		self._initstrategy = p0  # The player should have an initial strategy
		self._strategy = {}      # The player can distinguish each other in the base model so the strategies stored in a dictionary
		self._points = 0         # The initial score of the player is 0
		self._type = Type

		self._history = {}       # The playing history of the players
		self._myhistory = {}     # The playing history of the player self

		#--For Bayesian Type--#
		self._matrix = np.matrix([[1., 0.], [0., 1.]])
		#---------------------#

	def index(self):             # Get id of the player
		return self._id

	def getType(self):
		return self._type

	def initstrategy(self):
		return self._initstrategy

	def strategy(self, idx = -1):
		if idx == -1:                    # Default return the strategy
			return self._strategy
		else:                            # Return the certain strategy
			return self._strategy[idx]

	def add_strategy(self, idx):         # Add a new strategy if it not exists
		self._strategy[idx] = self._initstrategy

	#----------------To be implenmented----------------#
	def modify_strategy(self, idx, my_action, ad_action):
		if self.getType() == "Constant":
			pass
		elif self.getType() == "Random":
			new_strategy = rnd.random()
			self._strategy[idx] = new_strategy
		elif self.getType() == "Action_based":
			if ad_action == 0:
				self._strategy[idx] = min(self._strategy[idx] + Ka * self.points(), 1.)
			else:
				self._strategy[idx] = max(self._strategy[idx] - Ka * self.points(), 0.)
		elif self.getType() == "TFT":
			if ad_action == 0:
				self._strategy[idx] = 1.
			else:
				self._strategy[idx] = 0.
		elif self.getType() == "Co_TFT":
			if ad_action == 0:
				self._strategy[idx] = 1.
			else:
				if cBetray_times(self._history[idx]) > Kc:
					self._strategy[idx] = 0.
				else:
					self._strategy[idx] = 1.
		elif self.getType() == "Revenger":
			if ad_action == 1:
				self._strategy[idx] = 0.
		elif self.getType() == "Krevenger":
			if cBetray_times(self._history[idx]) > Kr:
				self._strategy[idx] = 0.
		elif self.getType() == "RKrevenger":
			if cBetray_times(self._history[idx]) > Krb:
				self._strategy[idx] = 0.
			elif cCoop_times(self._history[idx]) > Krc:
				self._strategy[idx] = 1.
		elif self.getType() == "Bayesian":
			self._matrix[0, 0] = p11(self._history[idx], self._myhistory[idx])
			self._matrix[0, 1] = p12(self._history[idx], self._myhistory[idx])
			self._matrix[1, 0] = p21(self._history[idx], self._myhistory[idx])
			self._matrix[1, 1] = p22(self._history[idx], self._myhistory[idx])
			old_p = np.matrix([[self.strategy(idx)], [1 - self.strategy(idx)]])
			new_p = np.dot(self._matrix, old_p)
			self._strategy[idx] = new_p[0, 0]
	#----------------To be implenmented----------------#

	def points(self):
		return self._points

	def add_points(self, u):
		self._points += u

	def playwith(self, adversary):
		if adversary.index() in self.strategy():
			pass
		else:
			self.add_strategy(adversary.index())
		action = rnd.random()
		if action <= self.strategy(adversary.index()):
			return 0                     # 0 means cooperation
		else:
			return 1                     # 1 means betrayal

	def update_history(self, adversary, ad_action, my_action):
		if adversary.index() in self._history:
			self._history[adversary.index()][0] += 1				# Playing times add 1
			self._history[adversary.index()][1] += ad_action		# Times betrayal add 1
			self._history[adversary.index()].append(ad_action)
			self._myhistory[adversary.index()][0] += 1				# Playing times add 1
			self._myhistory[adversary.index()][1] += my_action		# Times betrayal add 1
			self._myhistory[adversary.index()].append(my_action)
		else:
			self._history[adversary.index()] = [1]					# Playing times be 1
			self._history[adversary.index()].append(ad_action)		# Betrayal times
			self._history[adversary.index()].append(ad_action)
			self._myhistory[adversary.index()] = [1]				# Playing times be 1
			self._myhistory[adversary.index()].append(my_action)	# Betrayal times
			self._myhistory[adversary.index()].append(my_action)

# Class for the game
class game:
	def __init__(self, n, p0, M, Types, Prop):
		#---------------Need Modified---------------#
		self.utility = M                         # The utility matrix for each game
		self._population = n                     # The number of players is a certain number in the base model
		self._players = []                       # Generate the list of players where each has an id
		p = int(Prop * n)
		for i in range(p):
			self._players.append(player(i, 0.5, Types[0]))
		for i in range(p, n):
			self._players.append(player(i, p0, Types[1]))
		#---------------Need Modified---------------#

	def population(self):            # Get the number of the players
		return self._population

	def players(self, idex):         # Visit a player of a certain index
		return self._players[idex]

	def play(self, rounds, m):       # Play the game with a certain rounds and for each rounds there is m times match
		# Initialize the data set needs recording
		d_actions = [[-1] * rounds for i in range(self.population())]  # -1 indicates doing nothing
		                                                               # 0 will indicate cooperation
		                                                               # 1 will indicate betrayal
		d_points = [[0] * rounds for i in range(self.population())]    # The points of each player after each round
		d_strategys = [[{} for j in range(rounds)] for i in range(self.population())]
																	   # The strategy of each player after each round

		for i in range(rounds):
			played = set([])
			for j in range(m):
				id_a = rnd.randint(0, self.population() - 1)  # Player one
				while id_a in played:
					id_a = rnd.randint(0, self.population() - 1)
				played.add(id_a)

				id_b = rnd.randint(0, self.population() - 1)  # Player two
				while id_b in played:                         # Player two should not be the same as player one
					id_b = rnd.randint(0, self.population() - 1)
				played.add(id_b)

				action_a = self.players(id_a).playwith(self.players(id_b)) # The action of player one
				action_b = self.players(id_b).playwith(self.players(id_a)) # The action of player two

				#print("a: "+str(action_a))
				#print("b: "+str(action_b))
				
				self.players(id_a).add_points(self.utility[0][action_a][action_b]) # Update the score of player one
				self.players(id_b).add_points(self.utility[1][action_a][action_b]) # Update the score of player two

				self.players(id_a).update_history(self.players(id_b), action_b, action_a) # Update the history of player one
				self.players(id_b).update_history(self.players(id_a), action_a, action_b) # Update the history of player two

				#print(self.players(id_a)._history)
				#print(self.players(id_b)._history)

				#---------These two claues need modifying(and also maybe their position)---------#
				self.players(id_a).modify_strategy(id_b, action_a, action_b)
				self.players(id_b).modify_strategy(id_a, action_b, action_a)
				#---------These two claues need modifying(and also maybe their position)---------#

				# Record data into the data set
				# Actions
				d_actions[id_a][i] = action_a
				d_actions[id_b][i] = action_b
			# Points
			for j in range(self.population()):
				d_points[j][i] = self.players(j).points()
				# Strategy
				d_strategys[j][i] = deepcopy(self.players(j).strategy())

		# Return the data sets
		return d_actions, d_points, d_strategys


#---------------Main program goes from here----------------#
if __name__ == '__main__':
	for i in range(9):
		for j in range(11):
			print("Initializing...")
			new_game = game(N, P[j], U, T, PT[i])

			print("Simulating...")
			(actions_data, points_data, strategys_data) = new_game.play(R, M)

			print("Writing Results...")
			wdata_points(points_data, i, j)
			wdata_actions(actions_data, i, j)

			print("Done")

"""
Written by Will Longabaugh
"""

import gilmorelawler
from random import *

class Ant:
	# x in self.choices = (location, activity)
	# convention throughout will be that in pairs, location comes first, then activity 


	def __init__(self, alpha, distances, flows, n):
		self.distances = distances
		self.flows = flows
		self.n = n
		self.alpha = alpha
		self.choices = []
		self.remaining = list(range(n))


	def calcProbs(self, loc, traces):
		"""
		Gilmore-Lalwer module written by Michael Curry
		"""
		# Takes location we're trying to populate. Gets probabilities for placing unused activities at that location.
		probs = []

		# ind is a list of individual scores for placements
		ind = []
		for x in self.remaining:
			#print('trace contribution: ' + str(self.alpha*traces[loc][x]))
			#print('gl contribution: ' + str(((1-self.alpha)*(1/gilmorelawler.lbpartial(self.distances, self.flows, self.choices+[x])))))
			#print('trace to gl for activity %i at location %i: ' % (x, loc) + str((self.alpha*traces[loc][x])/((1-self.alpha)*(1/gilmorelawler.lbpartial(self.distances, self.flows, self.choices+[x])))))
			ind.append((x, (self.alpha*traces[loc][x]) + ((1-self.alpha)*(1/gilmorelawler.lbpartial(self.distances, self.flows, self.choices+[x])))))

		# total is the sum of all individual scores for placements, used for getting probabilities
		total = 0
		for x in ind:
			total += x[1]

		# lastnum will be used to give us probability range used in placement()
		lastnum = 0
		for x in ind:
			y = x[1]/total
			probs.append(((lastnum, lastnum+y), x[0]))
			lastnum += y

		return probs


	def placeActivity(self, loc, traces):
		# Takes location we're trying to populate. Uses a random number to choose which activity to put in the location.
		choice = ()
		x = self.calcProbs(loc, traces)
		y = random()
		for z in range(len(x)):
			if (y >= x[z][0][0]) and (y < x[z][0][1]):
				choice = x[z][1]
		self.choices.append(choice)
		self.remaining.remove(choice)


	def cleanUp(self):
		self.choices = []
		self.remaining = list(range(self.n))


	def populate(self, traces):
		for x in range(self.n):
			self.placeActivity(x, traces)


























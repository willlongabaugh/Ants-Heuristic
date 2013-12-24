# args: file name, repetitions, # ants, alpha, rho
"""
Written by Will Longabaugh
"""
import ant
import sys
import itertools

def readfile(filename):
	pfile = open(filename, 'r')
	n = int(pfile.readline())
	pfile.readline()

	a = []

	for i in range(n):
		l = pfile.readline().split()
		l2 = []
		for s in l:
			l2.append(int(s))
		a.append(l2)
	    
	b = []

	pfile.readline()

	for i in range(n):
		l = pfile.readline().split()
		l2 = []
		for s in l:
			l2.append(int(s))
		b.append(l2)

	return n, a, b



def upperbound(v,w):
    vs = sorted(v)
    ws = sorted(w)
    sum = 0
    for x in [vs[i] * ws[i] for i in range(len(v))]:
        sum = sum + x
    return sum



class antsystem:

	def __init__(self, x, repetitions, antnum, alpha, rho, bestscore):
		self.n = x[0]
		self.distances = x[1]
		self.flows = x[2]
		self.traces = [[0 for x in range(self.n)] for x in range(self.n)]
		self.repetitions = repetitions
		self.antnum = antnum
		self.alpha = alpha
		self.rho = rho
		self.bestscore = bestscore
		self.bestperm = []



	def calcscore(self, choices):
		score = 0
		for i in range(self.n):
			for h in range(i, self.n):
				score += self.distances[i][h]*self.flows[choices[i]][choices[h]]
		return score*2

	def updatetrace(self, cv, first):
		#lint = self.bestscore/cv[1]
		#augt = (self.bestscore/cv[1])*((self.bestscore/cv[1])**(1/2.0))
		quadt = (self.bestscore/cv[1])**2

		#if (not first):
		#	print('linear trace: ' + str(lint))
		#	print('augmented trace: ' + str(augt))
		#	print('quadratic trace: ' + str(quadt))
		#else:
		#	print('first linear trace: ' + str((lint/3))
		#	print('first augmented trace: ' + str(augt/(self.n/4)) )
		#	print('first quadratic trace: ' + str(quadt/(self.n/3)) )
		#print()

		for x in range(self.n):
			#if(not first):
			#	self.traces[cv[0][x]][cv[0].index(x)] += lint
			#else:
			#	self.traces[cv[0][x]][cv[0].index(x)] += lint/3

			#if(not first):
			#	self.traces[cv[0][x]][cv[0].index(x)] += augt
			#else:
			#	self.traces[cv[0][x]][cv[0].index(x)] += augt/(self.n/4)

			if(not first):
				self.traces[cv[0][x]][cv[0].index(x)] += quadt
			else:
				self.traces[cv[0][x]][cv[0].index(x)] += quadt/(self.n/3)



	def twoexchange(self, choices):
		"""
		Written by Daniel Webber
		"""
		bestVal = self.calcscore(choices)
		bestPerm = choices

		for i in range(self.n):
			for j in range(i, self.n):
				if i != j:
					newPerm = choices[:i]+[choices[j]]+choices[i+1:j]+[choices[i]]+choices[j+1:]
					newVal = self.calcscore(newPerm)
					if newVal < bestVal:
						bestVal = newVal
						bestPerm = newPerm
		return bestPerm, bestVal

	def itertwoexchange(self, n, choices):
		"""
		Written by Daniel Webber
		"""
		for i in range(n):
			lastchoices = choices
			choices, val = self.twoexchange(choices)
			if(choices==lastchoices):
				break
		return choices, val

	def decompose(self):
		self.traces = [[x*self.rho for x in y] for y in self.traces]
		#print('decomposed traces:\n' + str(self.traces))

	def genants(self):
		ants = []
		for x in range(self.antnum):
			ants.append(ant.Ant(self.alpha, self.distances, self.flows, self.n, self.traces))
		return ants

	def go(self):
		ants = self.genants()
		count = 0
		bestant = 0
		bestiter = 0
		for x in range(self.repetitions):
			print()
			print('repetition ' + str(x))
			for y in ants:
				y.populate(self.traces)
				#print('ant initial choices: ' + str(y.choices))
				cv = self.itertwoexchange(25, y.choices)
				#cv = (y.choices, self.calcscore(y.choices))
				print('iter choices: ' + str(cv))
				if(x+count == 0):
					self.updatetrace(cv, True)
				else:
					self.updatetrace(cv, False)
				if cv[1]<self.bestscore:
					print()
					print('best score update: ' + str(cv[1]))
					print()
					self.bestscore = cv[1]
					self.bestperm = cv[0]
					bestant = count
					bestiter = x
				y.cleanUp()
				count += 1
			count = 0
			self.decompose()

		print('Final Best Score: ' + str(self.bestscore))
		print('Final Best Permutation: ' + str(self.bestperm))
		print('Best Permutation found on Iteration: ' + str(bestiter+1) + ' By Ant: ' + str(bestant+1))




x = readfile(sys.argv[1])
y = list(itertools.chain.from_iterable(x[1]))
z = list(itertools.chain.from_iterable(x[2]))
bestscore = upperbound(y, z)
print('upperbound: ' + str(bestscore))
doit = antsystem(x, int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), bestscore)
doit.go()




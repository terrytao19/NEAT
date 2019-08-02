import numpy as np

class Net():
	def create(self):
		self.gene = [[[1],[7],[.2],[1],[1]],
    				 [[2],[8],[.7],[1],[2]],
    				 [[3],[7],[.4],[1],[3]],
    				 [[4],[9],[.1],[1],[4]],
    				 [[7],[6],[.9],[1],[5]],
    				 [[8],[9],[.8],[1],[6]],
    				 [[9],[6],[.5],[1],[7]],
    				 [[8],[5],[1],[1],[8]]]

	def sig(self, x, derivative = False):
		sigm = 1. / (1. + np.exp(-x))
		if derivative:
			return(sigm * (1. - sigm))
		return(sigm)

	def findio(self, value, i = False, o = False):
		allfound = []
		if i is True:
			for connection in self.gene:
				for incon in connection[0]:
					if value in incon:
						allfound.append(connection)
		if o is True:
			for connection in self.gene:
				for outcon in connection[1]:
					if type(outcon) is int:
						outcon = [outcon]
					if value in outcon:
						allfound.append(connection)

		return(allfound)


	def compute(self, node, observation):
		sigWE = 0
		if node == 0: return(observation[0])
		elif node == 1: return(observation[1])
		elif node == 2: return(observation[2])
		elif node == 3: return(observation[3])
		else:
			allfound = self.findio(o = True, value = node)
			for connection in allfound:
				if connection[3][0]:
					E = []
					E.append(self.compute(node = connection[0][0], observation = observation))
					E = sum(E)
					WE = E * connection[2][0]
					sigWE = self.sig(WE)
			return(sigWE)

agent = Net()
agent.create()
print(agent.compute(6, [-1.0,.5,20,.7]))
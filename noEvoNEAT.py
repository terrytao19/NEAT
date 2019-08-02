'''
nodes 1,2,3 and 4 are input nodes
nodes 5 and 6 are output nodes
'''

import numpy as np

class Net():
	def create(self):
		#Manually set genes, haven't gotten to the evolution step yet
		#[[in-node,out-node,weight,activated,innovation]]
		self.gene = [[1,7,.2,1,1],
    				 [2,8,.7,1,2],
    				 [3,7,.4,1,3],
    				 [4,9,.1,1,4],
    				 [7,6,.9,1,5],
    				 [8,9,.8,1,6],
    				 [9,6,.5,1,7],
    				 [8,5,1,1,8]]
		
	#sigmoid as activation function
	def sig(self, x, derivative = False):
		sigm = 1. / (1. + np.exp(-x))
		if derivative:
			return(sigm * (1. - sigm))
		return(sigm)
	
	#findio() finds all the connection genes that contain a specific connected node
	#example: node 7 is the output node of connection gene with innovation number of 3
	def findio(self, value, i = False, o = False):
		allfound = []
		if i is True:
			for connection in self.gene:
				incon = connection[0]
				if value in incon:
					allfound.append(connection)
		if o is True:
			for connection in self.gene:
				outcon = connection[1]
				if type(outcon) is int:
					outcon = [outcon]
				if value in outcon:
					allfound.append(connection)

		return(allfound)

	#compute() calculates the final value of any node, using recursion.
	#recursion is used in order to ensure that all the values have been calculated for the previous nodes before calculating the next.
	def compute(self, node, observation):
		sigWE = 0
		#Critical to recursion, similar to recursive fibonacci algorthm, sets the "base" / input values
		if node == 0: return(observation[0])
		elif node == 1: return(observation[1])
		elif node == 2: return(observation[2])
		elif node == 3: return(observation[3])
		else:
			allfound = self.findio(o = True, value = node)
			for connection in allfound:
				if connection[3]:
					E = []
					E.append(self.compute(node = connection[0], observation = observation))
					E = sum(E)
					WE = E * connection[2]
					sigWE = self.sig(WE)
			return(sigWE)

agent = Net()
agent.create()
			#This is the observation, or 4 inputs
print(agent.compute(6, [-1.0,.5,20,.7]))
		   #5 and 6 represent the output nodes, we are calculating their values
print(agent.compute(5, [-1.0,.5,20,.7]))

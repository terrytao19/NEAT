 
'''
nodes 1,2,3 and 4 are input nodes
nodes 5 and 6 are output nodes
'''

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

NUMBER_INPUT_NODES = 4
NUMBER_OUTPUT_NODES = 2

class Net():
	def create(self):
		#Manually set genes, haven't gotten to the evolution step yet
		#[[in-node,out-node,weight,activated,innovation]]
		self.gene = [[0,6,.2,1,1],
    				 [1,7,.7,1,2],
    				 [2,6,.4,1,3],
    				 [3,8,.1,1,4],
    				 [6,5,.9,1,5],
    				 [7,8,.8,1,6],
    				 [8,5,.5,1,7],
    				 [7,4,.1,1,8],
    				 [6,7,.8,1,8],
    				 [8,6,.7,1,8]]
		
	#sigmoid as activation function
	def sig(self, x, derivative = False):
		sigm = 1. / (1. + np.exp(-x))
		if derivative:
			return(sigm * (1. - sigm))
		return(sigm)
	
	#findio() finds all the connection genes that contain a specific output connected node
	def findio(self, value):
		allfound = []
		for connection in self.gene:
			outcon = connection[1]
			if type(outcon) is int:
				outcon = [outcon]
			if value in outcon:
				allfound.append(connection)
		return(allfound)

	def findNodeValue(self, node):
		for index,n in enumerate(self.listOfNodeValues):
			if node == n[0]:
				return(n,index)

	def resetNodeList(self):
	  	#tracks the value of each node, used for looping networks
		self.listOfNodeValues = []
		for c in self.gene:
			if c[0] not in [con[0] for con in self.listOfNodeValues] and c[0] not in range(NUMBER_INPUT_NODES):
				self.listOfNodeValues.append([c[0],0,0])
			if c[1] not in [con[0] for con in self.listOfNodeValues] and c[0] not in range(NUMBER_INPUT_NODES, NUMBER_INPUT_NODES + NUMBER_OUTPUT_NODES):
				self.listOfNodeValues.append([c[1],0,0])

	#compute() calculates the final value of any node, using recursion.
	#recursion is used in order to ensure that all the values have been calculated for the previous nodes before calculating the next.
	
	def compute(self, node, observation):
		sigWE = 0
		#Critical to recursion, similar to recursive fibonacci algorthm, sets the "base" / input values
		for n in range(NUMBER_INPUT_NODES):
			if n == node:
				return(observation[n])

		nodeVal, index = self.findNodeValue(node)
		if nodeVal[2]:
			return(nodeVal[2])

		allfound = self.findio(node)

		self.listOfNodeValues[index][2] = 1

		for connection in allfound:
			if connection[3]:
				E = []
				E.append(self.compute(node = connection[0], observation = observation))
				E = sum(E)
				WE = E * connection[2]
				sigWE = self.sig(WE)
		self.listOfNodeValues[index][1] = sigWE
		return(sigWE)

	def displayNet(self):
		G = nx.DiGraph()
		pos = {}
		edgeList = []
		for c in sorted(self.gene):
			edgeList.append([c[0],c[1]])
		G.add_edges_from(edgeList)
		for n in range(NUMBER_INPUT_NODES):
			pos[n] = (0,(500/NUMBER_INPUT_NODES)*n)
		for n in range(NUMBER_INPUT_NODES,NUMBER_OUTPUT_NODES+NUMBER_INPUT_NODES):
			pos[n] = (500,(500/NUMBER_OUTPUT_NODES)*n-1000)
		for n in range(NUMBER_INPUT_NODES + NUMBER_OUTPUT_NODES, len(self.listOfNodeValues)+NUMBER_INPUT_NODES):
			pos[n] = (np.random.randint(100,400),np.random.randint(100,400))
		print(pos)
		nx.draw(G, pos, with_labels=True, node_size=150)
		plt.show()

agent = Net()
agent.create()
			#This is the observation, or 4 inputs
agent.resetNodeList()
print(agent.compute(5, [-1.0,.5,20,.7]))
		   #5 and 6 represent the output nodes, we are calculating their values
agent.resetNodeList()
print(agent.compute(4, [-1.0,.5,20,.7]))
agent.displayNet()
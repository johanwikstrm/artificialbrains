from pybrain.structure import LinearLayer, SigmoidLayer, FeedForwardNetwork, FullConnection, BiasUnit

class Brain(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_HIDDENNODES_L1 = 8
	G_HIDDENNODES_L2 = 8
	G_OUTPUTNODES = 2
	G_TOTAL_CONNECTIONS = G_INPUTNODES * G_HIDDENNODES_L1 + G_HIDDENNODES_L1 * G_HIDDENNODES_L2 + G_HIDDENNODES_L2 * G_OUTPUTNODES + G_HIDDENNODES_L1 + G_HIDDENNODES_L2 + G_OUTPUTNODES

	def __init__(self, genes=None):
		self.net = FeedForwardNetwork()

		inLayer = LinearLayer(Brain.G_INPUTNODES, name='input')
		hiddenLayer1 = SigmoidLayer(Brain.G_HIDDENNODES_L1, name='hidden1')
		hiddenLayer2 = SigmoidLayer(Brain.G_HIDDENNODES_L2, name='hidden2')
		outLayer = SigmoidLayer(Brain.G_OUTPUTNODES, name='out')
		bias = BiasUnit(name='bias')

		self.net.addInputModule(inLayer)
		self.net.addModule(hiddenLayer1)
		self.net.addModule(hiddenLayer2)
		self.net.addModule(bias)
		self.net.addOutputModule(outLayer)

		in_to_hidden1 = FullConnection(inLayer, hiddenLayer1)
		hidden1_to_hidden2 = FullConnection(hiddenLayer1, hiddenLayer2)
		hidden2_to_out = FullConnection(hiddenLayer2, outLayer)
		bias_to_hidden1 = FullConnection(bias, hiddenLayer1)
		bias_to_hidden2 = FullConnection(bias, hiddenLayer2)
		bias_to_out = FullConnection(bias, outLayer)
		
		self.net.addConnection(in_to_hidden1)
		self.net.addConnection(hidden1_to_hidden2)
		self.net.addConnection(hidden2_to_out)
		self.net.addConnection(bias_to_hidden1)
		self.net.addConnection(bias_to_hidden2)
		self.net.addConnection(bias_to_out)

		self.net.sortModules()

		if genes != None:
			self.import_genes(genes)

	def think(self, data):
		return self.net.activate(data)

	def import_genes(self, genes):
		modules = self.net.modules
		connections = self.net.connections
		consumed_params = 0

		for module in modules:
			for conn in connections[module]:
				for i in xrange(len(conn.params)):
					conn.params[i] = genes[consumed_params]	
					consumed_params += 1

	def examine_brain(self):
		modules = self.net.modules
		
		connections = self.net.connections

		print " == Creature == "
		for module in modules:
			print "%s:" % module
			for conn in connections[module]:
				print " 	%s" % conn
				print "%s" % conn.params

# Inputs:
# 5 for first antennae, i.e. antennae_angles[0]
# 0: Object detection, 1 if detected 0 if not
# 1: R 0 - 1
# 2: G 0 - 1
# 3: B 0 - 1
# 4: Object detection 2...
import random

class BrainRandom(object):
	"""docstring for Brain"""
	G_INPUTNODES = 8
	G_TOTAL_CONNECTIONS = 1 # 12 calls * 3 genes
	G_GENES_NEEDED = G_TOTAL_CONNECTIONS + 3
	G_REGION_SIZE = 1

	def __init__(self, genes=None):
		if genes is not None:
			self.import_genes(genes)

	def think(self, data):

		if data[0] == 0 and data[4] == 0:
			return (0.005, 0)
		
		else:
			return (random.random() * 2.0 - 1.0, random.random() * 2.0 - 1.0)

	# assuming that the last three genes are not used
	def import_genes(self, genes):
		self.genes = genes

	def diagnose(self):
		print "Random"
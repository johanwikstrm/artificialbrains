import unittest
import random
import operator
from brain_linear import BrainLinear
from brain_rbf import BrainRBF
import numpy as np

# Tests for Brain Linear are a bit broken
class BrainLinearTest(unittest.TestCase):
	def setUp(self):
		self.brain = BrainLinear()

	def test_zeroed_brain(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([0] * BrainLinear.G_TOTAL_CONNECTIONS)
		#print "Zeroed tests:"
		self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		self.assertEqual(self.brain.think([1] * ins), (0,0), 'Output with full input incorrect.')
		self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0,0), 'Output with full input to left incorrect.')
		self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0,0), ' Output with full input to right incorrect.')

		self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0,0), 'Output when not detecting 1 color incorrect.')

		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0,0), 'Output when not detecting 1 color incorrect.')
		self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0,0), 'Output when not detecting 1 color incorrect.')

	def test_left_antenna(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([1] * (BrainLinear.G_TOTAL_CONNECTIONS / 2) + [0] * (BrainLinear.G_TOTAL_CONNECTIONS / 2))
		#print "Left tests:"
		# self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		# self.assertEqual(self.brain.think([1] * ins), (1.0,1.0), 'Output with full input incorrect.')
		# self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0.5,0.5), 'Output with full input to left incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0,0), 'Output with full input to right incorrect.')		

		# self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')

		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0,0), 'Output when not detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0,0), 'Output when not detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0,0), 'Output when not detecting 1 color incorrect.')

	def test_right_antenna(self):
		ins = BrainLinear.G_INPUTNODES
		self.brain.import_genes([0] * (BrainLinear.G_TOTAL_CONNECTIONS / 2) + [1] * (BrainLinear.G_TOTAL_CONNECTIONS / 2))
		#print "Right tests:"
		# self.assertEqual(self.brain.think([0] * ins), (0.005,0), 'Output when detecting nothing is incorrect.')
		# self.assertEqual(self.brain.think([1] * ins), (0.5,0.5), 'Output with full input incorrect.')
		# self.assertEqual(self.brain.think([1] * (ins/2) + [0] * (ins/2)), (0,0), 'Output with full input to left incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins/2) + [1] * (ins/2)), (0.5,0.5), 'Output with full input to right incorrect.')				

		# self.assertEqual(self.brain.think([1] * 2 + [0] * (ins - 2)), (0,0), 'Output when not detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([1] + [0] + [1] + [0] * (ins - 3)), (0,0), 'Output when not detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([1] + [0] * 2 + [1] + [0] * (ins - 4)), (0,0), 'Output when not detecting 1 color incorrect.')

		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] * 2 + [0] * 2), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] + [1] + [0]), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
		# self.assertEqual(self.brain.think([0] * (ins / 2) + [1] + [0] * 2 + [1]), (0.5/3,0.5/3), 'Output when only detecting 1 color incorrect.')
	def test_fuzz(self):
		print "Linear:"
		num_tests = 10000
		ins = BrainLinear.G_INPUTNODES
		res = [0]*num_tests 
		for i in xrange(num_tests) :
			
			self.brain.import_genes(map(lambda x: random.random()*x*2-1, [1]*(BrainLinear.G_TOTAL_CONNECTIONS+3)))
			res[i] = self.brain.think(map(lambda x: random.random()*x, [1]*ins))
			a = res[i]
			self.assertTrue(res[i][0] >= -1 and res[i][0] <= 1, "Value range invalid: %f" % (res[i][0]))
			self.assertTrue(res[i][1] >= -1 and res[i][1] <= 1, "Value range invalid: %f" % (res[i][1]))
			
		#print 'random weights, random input %d vs %d' % (len([ds for (ds,dr) in res if ds > 0]) , num_tests - len([ds for (ds,dr) in res if ds > 0]))
		self.assertTrue(len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) > 0.45 and len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) < 0.55, "fuzz testing gave abnormal distribution of results")
		res_a = np.array(res)
		print "10th percentile: %f" % (np.percentile(res_a, 10))
		print "25th percentile: %f" % (np.percentile(res_a, 25))
		print "50th percentile: %f" % (np.percentile(res_a, 50))
		print "75th percentile: %f" % (np.percentile(res_a, 75))
		print "90th percentile: %f" % (np.percentile(res_a, 90))


	def tearDown(self):
		del self.brain

class BrainRBFTest(unittest.TestCase):
	def setUp(self):
		self.brain = BrainRBF()

	def test_fuzz(self):
		print "RBF:"
		num_tests = 10000
		ins = BrainRBF.G_INPUTNODES
		res = [0]*num_tests
		i = 0 
		while i < num_tests:
			self.brain.import_genes(map(lambda x: random.random()*x*2-1, [1] * (BrainRBF.G_GENES_NEEDED)))
			inputData = map(lambda x: random.random()*x, [1]*ins)			
			inputData[0] = round(inputData[0]) # should be 1 or 0
			inputData[4] = round(inputData[4]) # should be 1 or 0
			if inputData[0] == 0 and inputData[4] == 0 :
				i = i-1
				continue # no need to test on zero input, has default behaviour 
			res[i] = self.brain.think(inputData)
			self.assertTrue(res[i][0] >= -1 and res[i][0] <= 1, "Value range invalid: %f" % (res[i][0]))
			self.assertTrue(res[i][1] >= -1 and res[i][1] <= 1, "Value range invalid: %f" % (res[i][1]))
			i = i+1
		#print 'random weights, random input %d vs %d' % (len([ds for (ds,dr) in res if ds > 0]) , num_tests - len([ds for (ds,dr) in res if ds > 0]))
		self.assertTrue(len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) > 0.45 and len([ds for (ds,dr) in res if ds > 0]) / float(num_tests) < 0.55, "fuzz testing gave abnormal distribution of results %f vs %f" %(len([ds for (ds,dr) in res if ds > 0]) / float(num_tests),len([ds for (ds,dr) in res if ds < 0]) / float(num_tests)))
		res_a = np.array(res)
		print "10th percentile: %f" % (np.percentile(res_a, 10))
		print "25th percentile: %f" % (np.percentile(res_a, 25))
		print "50th percentile: %f" % (np.percentile(res_a, 50))
		print "75th percentile: %f" % (np.percentile(res_a, 75))
		print "90th percentile: %f" % (np.percentile(res_a, 90))

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()

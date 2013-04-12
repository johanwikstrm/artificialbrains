from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from deap import base,creator,tools
import random,time

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.uniform, -2, 2)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

DS = SupervisedDataSet(1,1)
DS.appendLinked([1],[-1])
DS.appendLinked([-0.83],[0.83])
DS.appendLinked([-0.3],[0.3])
DS.appendLinked([0.3],[-0.3])
DS.appendLinked([0.028], [-0.028])
DS.appendLinked([-1],[1])

def calcError(x, y):
	return abs(x - y) / x

def testNetwork(eVar):
	global net # So that we can look at the network after we're done training
	net = buildNetwork(1,1,1,bias=True,outputbias=True)
	
	net.connections[net['in']][0].params[0] = eVar[0];
	net.connections[net['hidden0']][0].params[0] = eVar[1];
	net.connections[net['bias']][0].params[0] = eVar[2];
	net.connections[net['bias']][1].params[0] = eVar[3];

	res = net.activateOnDataset(DS)
	fitness = 1
	for i in range(len(DS['target'])):
		absError = abs(calcError(res[i], DS['target'][i]))
		if absError <= 1:
			fitness += 1 - absError # Removes as many percent as the network is incorrect from the fitness
		else:
			fitness -= 1.0/len(DS) # If the network is too inaccurate it is instead punished

	return fitness

def runSimulation(pop):
	return [testNetwork(ind) for ind in pop]

def printStats(pop):
	fits = [ind.fitness.values[0] for ind in pop]
	mean = sum(fits) / len(pop)
	print ("Max: %s, Avg: %s, Min: %s" % (max(fits), mean, min(fits)))

toolbox.register("evaluate", testNetwork)
toolbox.register("mate", tools.cxUniform, indpb=0.05)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.7, indpb=0.1)
toolbox.register("select", tools.selRoulette)
toolbox.register("map",map)

NGEN=300
CXPB=0.7
MUTPB=0.7

def main():
	start = time.clock()

	pop = toolbox.population(n=100)

	# Evaluate our new population
	fitnesses = runSimulation(pop)
	for ind,fit in zip(pop,fitnesses):
		ind.fitness.values = fit,

	# Begin the evolution
	for g in range(NGEN):
		if g % 10 == 0 and g != 0:
			print "--Generation %d--" % (g)
			printStats(pop)

		# Select the next generation individuals
		offspring = toolbox.select(pop, len(pop))
		# Clone the selected individuals
		offspring = list(toolbox.map(toolbox.clone,offspring))

		# Apply crossover and mutation to the offspring
		#for child1,child2 in zip(offspring[::2],offspring[1::2]):
		#	if random.random() < CXPB:
		#		toolbox.mate(child1,child2)
		#		del child1.fitness.values
		#		del child2.fitness.values

		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values

		# Evaluate the fitness of the individuals with invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = runSimulation(invalid_ind)
		for ind,fit in zip(invalid_ind,fitnesses):
			ind.fitness.values = fit,

		pop[:] = offspring

	end = time.clock()

	printStats(pop)

	print "  Run-time %f" % (0.0 + end - start)

if __name__ == '__main__':
	main()
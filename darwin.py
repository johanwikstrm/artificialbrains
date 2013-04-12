import multiprocessing, platform, random, itertools, time, stats, funcs

import numpy as np
from deap import base,creator,tools
from brain_rbf import BrainRBF
from brain_linear import BrainLinear
from brain_random import BrainRandom
from world import World
from creature import Creature
from cPickle import Pickler, Unpickler
from numpy import array
	
if platform.python_implementation() != 'PyPy':
	from renderer import Renderer
	renderer_available = True
else:
	renderer_available = False

try: # Note: cTools are not compatible with PyPy
	from deap import cTools 
	cTools_available = True
except ImportError:
	cTools_available = False

def simulate(living,nticks=None, max_bush_count=None, max_red_bush_count=None):
	"""Used to run a simulation, placed outside of class to enable multiprocessing"""
	creatures = living[0]
	predators = living[1]

	w = World(gene_pool_creatures=creatures, gene_pool_predators=predators, nticks=nticks,max_bush_count=max_bush_count,max_red_bush_count=max_red_bush_count)
	w.run_ticks()
	return (w.get_creatures(), w.get_predators())

class Darwin(object):
	"""docstring for Darwin"""
	def check_bounds(self, min, max):
	    def decorator(func):
	        def wrapper(*args, **kargs):
	            offspring = func(*args, **kargs)
	            for child in offspring:
	                for i in xrange(len(child)):
	                    if child[i] > max:
	                        child[i] = max
	                    elif child[i] < min:
	                        child[i] = min
	            return offspring
	        return wrapper
	    return decorator

	def cross_over(self, child1, child2, indpb):
		genes1 = child1[0:-3]
		genes2 = child2[0:-3]

		for i in xrange(len(genes1), self.Brain.G_REGION_SIZE):
			if random.random() < indpb:
				genes1[i:i+self.Brain.G_REGION_SIZE], genes2[i:i+self.Brain.G_REGION_SIZE] = genes2[i:i+self.Brain.G_REGION_SIZE], genes1[i:i+self.Brain.G_REGION_SIZE]

		return genes1, genes2

	def __init__(self):
		if Darwin.graphics and renderer_available:
			self.renderer = Renderer()

		self.toolbox = base.Toolbox()
		self.gen_start_number = 1
		self.Brain = eval(Darwin.brain_type)

		creator.create("FitnessMax", base.Fitness, weights=(1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMax)

		self.toolbox.register("attr_float", random.uniform, -1, 1)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, self.Brain.G_TOTAL_CONNECTIONS + 3)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("mate", self.cross_over, indpb=0.3)
		self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=1.0/self.Brain.G_TOTAL_CONNECTIONS)
		
		self.toolbox.decorate("mutate", self.check_bounds(-1,1))

		self.toolbox.register("selectBest", tools.selBest)
		self.toolbox.register("simulate", simulate, nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count, max_red_bush_count=Darwin.max_red_bush_count)

		#if cTools_available:
		#	self.toolbox.register("select", cTools.selNSGA2)
		#else:
		self.toolbox.register("select", tools.selRoulette)

		self.pop = self.toolbox.population(n=Darwin.NINDS)
		self.pred_pop = self.toolbox.population(n=Darwin.NPRED)

		if Darwin.enable_multiprocessing:
			self.pool = multiprocessing.Pool(processes=3)
			self.toolbox.register("map",self.pool.map)
		else:
			self.toolbox.register("map",map)

	def evaluate(self, ind):
		return ind.life_length / 5

	def evolve_population(self, creatures, g):
		fitnesses = [self.evaluate(creature) for creature in creatures]
		pop = [creature.brain.genes for creature in creatures]

		for ind,fit in zip(pop, fitnesses):
			ind.fitness.values = fit,
		
		if creatures[0].predator == True:
			print "Predators: %s " % (self.printStatsPredators(pop,g))
		else:
			deaths_by_age = len([creature.cod for creature in creatures if creature.cod == 'age'])
			deaths_by_bush = len([creature.cod for creature in creatures if creature.cod == 'bush'])
			deaths_by_predator = len([creature.cod for creature in creatures if creature.cod == 'predator'])
			print "Creatures: %s " % (self.printStatsCreatures(pop,g,deaths_by_age,deaths_by_bush,deaths_by_predator))
		
		#if g % 10 == 0 or g == self.gen_start_number:
		#		self.printGeneStats(pop)
		#		self.printBrainStats(self.toolbox.selectBest(pop,1))

		bestInds = self.toolbox.selectBest(pop, len(pop) / 10)
		bestInds = list(self.toolbox.map(self.toolbox.clone, bestInds))
		offspring = self.toolbox.select(pop, len(pop) * 9 / 10)
		offspring = list(self.toolbox.map(self.toolbox.clone, offspring))			

		for child1,child2 in zip(offspring[::2],offspring[1::2]):
			if random.random() < Darwin.CXPB:
				self.toolbox.mate(child1,child2)

		for mutant in offspring:
			if random.random() < Darwin.MUTPB:
				self.toolbox.mutate(mutant)

		pop = bestInds + offspring

		for ind in pop:
			del ind.fitness.values

		return pop

	def begin_evolution(self):

		# Begin actual evolution
		start_time = time.time()
		
		pop = self.pop
		pred_pop = self.pred_pop

		for g in xrange(self.gen_start_number,self.gen_start_number+Darwin.NGEN):

			creatures, predators = self.simulate(pop, pred_pop)

			pop = self.evolve_population(creatures, g)
			
			if len(pred_pop) > 0:
				pred_pop = self.evolve_population(predators, g)

			if g % 20 == 0:
				self.printTimeStats(start_time, g)
			
		self.pop = pop
		self.pred_pop = pred_pop

		self.gen_start_number = g
		f = open(Darwin.save_file,'w')
		self.save_population(f)
		stats.save_stats(open('stats_' + Darwin.save_file,'w'))

		stats.plot_all()
	
	def simulate(self, creature_pop, predator_pop):
		res = []
		ips = Darwin.num_inds_per_sim
		pps = Darwin.NPRED * ips / Darwin.NINDS

		if len(creature_pop) > Darwin.num_inds_per_sim:
			inputs = [(creature_pop[i * ips:(i+1) * ips], predator_pop[i * pps:(i+1) * pps]) for i in xrange(0,len(creature_pop)/ips)]

			if Darwin.graphics and renderer_available:
				if Darwin.enable_multiprocessing:
					res += self.renderer.play_epoch(World(gene_pool_creatures=inputs[0][0], gene_pool_predators=inputs[0][1], nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count, max_red_bush_count=Darwin.max_red_bush_count))
					res += list(itertools.chain(*self.toolbox.map(self.toolbox.simulate, inputs[1:])))
				else:
					for i in inputs:
						res += self.renderer.play_epoch(World(gene_pool_creatures=i[0], gene_pool_predators=i[1], nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count, max_red_bush_count=Darwin.max_red_bush_count))
			else:
				res = list(itertools.chain(*self.toolbox.map(self.toolbox.simulate, inputs)))
			
			c_res = []
			r_res = []
			#Fulhack!
			for i in xrange(0,len(res),2):
				c_res += res[i]
				r_res += res[i+1]
			
			res = (c_res, r_res)

		else:
			if Darwin.graphics and renderer_available:
				res = self.renderer.play_epoch(World(gene_pool_creatures=creature_pop, gene_pool_predators=predator_pop, nticks=Darwin.NTICKS, max_bush_count=Darwin.max_bush_count, max_red_bush_count=Darwin.max_red_bush_count))
			else:
				res = self.toolbox.simulate((creature_pop,predator_pop))

		return res

	def save_population(self,save_file):
		pickler = Pickler(save_file)
		data = (self.pop, self.pred_pop, self.gen_start_number + 1)
		pickler.dump(data)
		save_file.close()

	def load_population(self,load_file):
		unpickler = Unpickler(load_file)
		self.pop, self.pred_pop, self.gen_start_number = unpickler.load()
		load_file.close()

	def load_stats(self,load_stats_file):
		stats.load_stats(load_stats_file)

	def printGeneStats(self,pop):
		genes = np.array(pop)
		stds = np.std(genes,0)
		print "# Gene stats"
		print "Avg std: %5.2f" % (np.mean(stds))

	def printBrainStats(self,bestInd):
		print "# Brain diagnosis of best individuals rotation:"
		b = self.Brain(bestInd[0])
		b.diagnose()

	def printTimeStats(self,start_time,gen):
		time_spent = time.time() - start_time
		avg = time_spent / (gen + 1 - self.gen_start_number)
		generations_left = (self.gen_start_number + Darwin.NGEN - gen)
		print '\033[95m' + "# Time stats: Spent: %2.2f s, Avg/gen: %2.2f s" % (time_spent, avg)
		print "# Time to run %i gens: %2.2f s" % (generations_left, generations_left * avg), '\033[0m'

	def printStatsPredators(self,pop,gen):
		fits = [ind.fitness.values[0] for ind in pop]
		mean = sum(fits) / len(pop)
		stats.add("predator_fitness.avg",mean)
		stats.add("predator_fitness.min",min(fits))
		stats.add("predator_fitness.max",max(fits))
		return ("(%3i): Max: %6.2f, Avg: %6.2f, Min: %5.2f" % (gen, max(fits), mean, min(fits)))

	def printStatsCreatures(self,pop,gen,dba,dbb,dbp):
		fits = [ind.fitness.values[0] for ind in pop]
		mean = sum(fits) / len(pop)
		reds = [funcs.gene2color(genome[-1]) for genome in pop]
		greens = [funcs.gene2color(genome[-2]) for genome in pop]
		blues = [funcs.gene2color(genome[-3]) for genome in pop]
		stats.add("creature_fitness.avg",mean)
		stats.add("creature_fitness.min",min(fits))
		stats.add("creature_fitness.max",max(fits))
		stats.add("creature.death_by_bush_procent",dbb*1.0/(dbb+dba+dbp))
		stats.add("creature.death_by_predator_procent",dbp*1.0/(dbb+dba+dbp))
		stats.add("creature_color.red", sum(reds)/len(reds))
		stats.add("creature_color.blue", sum(blues)/len(blues))
		stats.add("creature_color.green", sum(greens)/len(greens))
		return ("(%3i): Max: %6.2f, Avg: %6.2f, Min: %5.2f, DBBP: %.2f" % (gen, max(fits), mean, min(fits),dbb*1.0/(dbb+dbp+dba)))

import random, funcs, math
from creature import Creature
from bush import Bush
from numpy import array
from brain_rbf import BrainRBF
from brain_linear import BrainLinear
from brain_random import BrainRandom

class World(object):
	"""docstring for ClassName"""
	def __init__(self, gene_pool_creatures=None, gene_pool_predators=None, max_bush_count=0, max_red_bush_count=0, nticks=10000):
		self.Brain = eval(World.brain_type)
		self.creatures = []
		self.dead_creatures = []
		self.predators = []
		self.dead_predators = []
		self.bushes = []
		self.red_bushes = []
		self.nticks = nticks
		if gene_pool_creatures is not None:
			for gene in gene_pool_creatures:
				if False:
					self.creatures += [Creature(gene, x=0.05, y=(0.1 + 0.1 * len(self.creatures)))]
					self.creatures[-1].rotation = 0
				else:
					self.creatures += [Creature(gene, x=random.uniform(0.05,0.95), y=random.uniform(0.05,0.95))]
		if gene_pool_predators is not None and gene_pool_predators != []:
			for gene in gene_pool_predators:
				self.predators += [Creature(gene, x=random.uniform(0.05,0.95), y=random.uniform(0.05,0.95),predator=True)]

		self.max_bush_count = max_bush_count
		self.max_red_bush_count = max_red_bush_count
		#self.spawn_bushes_grid()
		#self.spawn_bushes_line()

	def run_tick(self):
		self.spawn_bushes()

		# Get data for creatures to process
		inhabitants = []

		if World.detect_creatures:
			inhabitants += self.get_living()

		if World.detect_bushes:
			inhabitants += self.get_bushes()

		#inhabitants = self.bushes + self.red_bushes # Only detecting/colliding with bushes
		positions = array([inh.get_pos() for inh in inhabitants])
		radii = array([inh.get_radius() for inh in inhabitants])

		for creature in self.get_living():
			creature_pos = creature.get_pos()

			creature_got_input = False
			left = [0] * (self.Brain.G_INPUTNODES/2)
			right = [0] * (self.Brain.G_INPUTNODES/2)

			if len(positions) > 0:
				diffs = positions - creature_pos
				distances = array([funcs.special_vlen(diff) for diff in diffs]) - radii
				for index, val in enumerate(distances):
					if val <= creature.antennae_length and creature != inhabitants[index]:
						[left, right] = self.check_detection(creature,inhabitants[index])

					if val <= creature.get_radius() and creature != inhabitants[index]:
						creature.on_collision(inhabitants[index])
						inhabitants[index].on_collision(creature)
				
			if creature_pos[0] - creature.antennae_length < 0 or creature_pos[0] + creature.antennae_length > 1 or creature_pos[1] - creature.antennae_length < 0 or creature_pos[1] + creature.antennae_length > 1:
				[left, right] = self.detect_walls(creature, left, right)

			if left != [0] * (self.Brain.G_INPUTNODES/2) or right != [0] * (self.Brain.G_INPUTNODES/2):
				creature_got_input = True
				creature.gather_input(left + right)

			if World.default_input:
				if not creature_got_input:
					creature.gather_input(left + right)

		if World.think:
			for inhabitant in self.get_inhabitants():
				inhabitant.think()
		
		if World.move:
			for inhabitant in self.get_inhabitants():
				inhabitant.move()

		if World.remove_dead:
			for inhabitant in self.get_inhabitants():
				if inhabitant.alive == False:
					if inhabitant in self.creatures:
						self.creatures.remove(inhabitant)
						self.dead_creatures += [inhabitant]
					if inhabitant in self.predators:
						self.predators.remove(inhabitant)
						self.dead_predators += [inhabitant]

					if isinstance(inhabitant,Bush):
						if inhabitant.poisonous:
							self.red_bushes.remove(inhabitant)
						else:
							self.bushes.remove(inhabitant)

	def run_ticks(self):
		for tick in xrange(self.nticks):
			if len(self.creatures) != 0 or len(self.predators) != 0:
				self.run_tick()
			else:
				break

	def detect_walls(self, looker, left, right):
		looker_pos = looker.get_pos()

		angle = looker.rotation * 2 * math.pi
		if left == [0] * (self.Brain.G_INPUTNODES/2):
			v_an1 = [looker.antennae_length * math.cos(angle + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[0])]

			antennae_point1 = funcs.vplus(looker_pos, v_an1)

			if antennae_point1[0] < 0 or antennae_point1[0] > 1 or antennae_point1[1] < 0 or antennae_point1[1] > 1:
				left[0] = 1
				left[1], left[2], left[3] = [0,0,1]

		if right == [0] * (self.Brain.G_INPUTNODES/2):
			v_an2 = [looker.antennae_length * math.cos(angle + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[1])]

			antennae_point2 = funcs.vplus(looker_pos, v_an2)

			if antennae_point2[0] < 0 or antennae_point2[0] > 1 or antennae_point2[1] < 0 or antennae_point2[1] > 1:
				right[0] = 1
				right[1], right[2], right[3] = [0,0,1]

		return left, right

	def check_detection(self,looker, target):
		invalid1 = False
		invalid2 = False

		inputs = self.Brain.G_INPUTNODES/2
		left = [0] * inputs
		right = [0] * inputs

		v_dist = funcs.vminus(target.get_pos(), looker.get_pos())

		angle = looker.rotation * 2 * math.pi
		v_an1 = array([looker.antennae_length * math.cos(angle + looker.antennae_angles[0]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[0])])
		v_an2 = array([looker.antennae_length * math.cos(angle + looker.antennae_angles[1]),
			-1 * looker.antennae_length * math.sin(angle + looker.antennae_angles[1])])
		
		an1_dist_sq = funcs.dot(v_an1, v_dist) / funcs.vlen(v_an1)**2
		an2_dist_sq = funcs.dot(v_an2, v_dist) / funcs.vlen(v_an2)**2
		v_proj1 = array([v_an1[0] * an1_dist_sq, v_an1[1] * an1_dist_sq])
		v_proj2 = array([v_an2[0] * an2_dist_sq, v_an2[1] * an2_dist_sq])

		# If the projection points in the exact opposite direction of the antenna no detection is possible
		if v_an1[0] > 0 and v_proj1[0] < 0 or v_an1[0] < 0 and v_proj1[0] > 0:
			invalid1 = True
		if v_an2[0] > 0 and v_proj2[0] < 0 or v_an2[0] < 0 and v_proj2[0] > 0:
			invalid2 = True

		# If the projection is longer than the antennae we pretend that the antennae is the projection to avoid false positives
		if funcs.vlen(v_proj1) > funcs.vlen(v_an1): 
			v_proj1 = v_an1
		if funcs.vlen(v_proj2) > funcs.vlen(v_an2):
			v_proj2 = v_an2

		dist_from_proj1 = funcs.vminus(v_proj1, v_dist)
		dist_from_proj2 = funcs.vminus(v_proj2, v_dist)

		if funcs.vlen(dist_from_proj1) < target.get_radius() and not invalid1:
			left[0] = 1
			left[1],left[2],left[3] = target.get_color()

		if funcs.vlen(dist_from_proj2) < target.get_radius() and not invalid2:
			right[0] = 1
			right[1],right[2],right[3] = target.get_color()
		
		return left, right

	def spawn_bushes(self):
		if len(self.bushes) < self.max_bush_count:
			for i in xrange(self.max_bush_count - len(self.bushes)):
				if random.random() < 0.05:
					self.bushes += [Bush(random.uniform(0.05,0.95), random.uniform(0.05,0.95))]

		if len(self.red_bushes) < self.max_red_bush_count:

			for i in xrange(self.max_red_bush_count - len(self.red_bushes)):
				if random.random() < 0.01:
					self.red_bushes += [Bush(random.uniform(0.05,0.95), random.uniform(0.05,0.95), poisonous=True)]

	def spawn_bushes_line(self):
		for i in xrange(16):
			if i % 2 == 0:
				self.bushes += [Bush(x=0.85,y=(0.07 + i * 0.05))]
			else:
				self.red_bushes += [Bush(x=0.85,y=(0.07 + i * 0.05),poisonous=True)]

	def spawn_bushes_grid(self):
		for i in xrange(1,5):
			for j in xrange(1,5):
				self.add_bush(Bush(i*0.2, j*0.2))

	def add_bush(self, bush):
		self.bushes += [bush]

	def add_creature(self, creature):
		self.creatures += [creature]

	def get_living(self):
		return self.creatures + self.predators

	def get_inhabitants(self):
		return self.creatures + self.predators + self.bushes + self.red_bushes

	def get_positions(self):
		return [creature.get_pos() for creature in self.creatures]

	def get_creatures(self):
		return self.creatures + self.dead_creatures

	def get_predators(self):
		return self.predators + self.dead_predators

	def get_bushes(self):
		return self.bushes + self.red_bushes

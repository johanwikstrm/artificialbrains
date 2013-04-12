from brain_rbf import BrainRBF
from brain_linear import BrainLinear
from brain_random import BrainRandom
from inhabitant import Inhabitant
import math, random, funcs

class Creature(Inhabitant):
	"""docstring for ClassName"""
	G_MAX_ROTATION = 0.5
	antennae = 2
	antennae_angles = [math.pi/6.0, -1.0 * math.pi/6.0]

	def __init__(self, genes=None, x=0.0, y=0.0, predator=False):
		
		R = funcs.gene2color(genes[-1])
		G = funcs.gene2color(genes[-2])
		B = funcs.gene2color(genes[-3])

		if predator:
			R,G,B = 0.9, 0.1, 0.1

		super(Creature, self).__init__([x,y], 
			radius_multiplier=0.5, 
			color=(R,G,B),
			energy=Creature.health)
			
		self.predator = predator
		self.cod = None
		self.rotation = random.random()
		self.speed = 0.0
		self.num_detections = 1
		self.distance = 0.0
		self.rotated = 0.0
		self.consumed_energy = 1
		self.life_length = 1
		self.antennae_length = self.radius_multiplier * self.G_MAXIMUM_RADIUS * 5
		self.brain = eval(Creature.brain_type)(genes)

	def gather_input(self, data):
		self.data = data

	def think(self):
		[d_s, d_r] = self.brain.think(self.data)

		#if d_r != 0:
			#print "Before: %f, d_r: %f" % (self.rotation, d_r)

		self.rotation = (self.rotation + d_r * Creature.G_MAX_ROTATION)

		if self.rotation < 0:
			self.rotation = 1 - (abs(self.rotation) % 1.0)
		if self.rotation > 1:
			self.rotation = self.rotation % 1.0

		#if d_r != 0:
			#print "After: %f" % self.rotation

		# self.rotation = funcs.sign(self.rotation + d_r * Creature.G_MAX_ROTATION) * (abs(self.rotation + d_r * Creature.G_MAX_ROTATION) % 1.0)
		self.speed += d_s
		if self.speed > 1.0:
			self.speed = 1.0
		if self.speed < -1.0:
			self.speed = -1.0

	# def think(self):
	# 	if self.data[2] > 0.6 and self.data[1] < 0.4 or self.data[6] > 0.6 and self.data[5] < 0.4 and self.speed > 0:
	# 		self.num_detections += 1

	# 	[d_s, d_r] = self.brain.think(self.data)
	# 	d_s = d_s * 2 - 1
	# 	d_r = d_r * 2 - 1

	# 	self.rotated += d_r
	# 	self.rotation = funcs.sign(self.rotation + d_r * Creature.G_MAX_ROTATION) * (abs(self.rotation + d_r * Creature.G_MAX_ROTATION) % 1.0)

	# 	self.speed += d_s
	# 	if self.speed > 1:
	# 		self.speed = 1
	# 	if self.speed < -1:
	# 		self.speed = -1

	def on_collision(self, target):
		if self.predator and isinstance(target,Creature) and not target.predator:
			self.energy += 150
			target.cod = 'predator'
			target.alive = False

	def move(self):
		self.energy -= 1
		self.life_length += 1
		if self.energy <= 0 and self.alive == True:
			self.alive = False
			self.cod = 'age'

		angle = self.rotation * 2.0 * math.pi
		d_x = math.cos(angle) * self.speed * self.G_MAX_SPEED
		d_y = -1.0 * math.sin(angle) * self.speed * self.G_MAX_SPEED
		self.pos[0] += d_x
		if self.pos[0] + self.get_radius() > 1:
			self.pos[0] = 1 - self.get_radius()
		elif self.pos[0] - self.get_radius() < 0:
			self.pos[0] = 0 + self.get_radius()
		self.pos[1] += d_y
		if self.pos[1] + self.get_radius() > 1:
			self.pos[1] = 1 - self.get_radius()
		elif self.pos[1] - self.get_radius() < 0:
			self.pos[1] = 0 + self.get_radius()
		self.distance += math.sqrt(d_x**2 + d_y**2)

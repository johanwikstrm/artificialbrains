from numpy import array

class Inhabitant(object):
	"""docstring for Inhabitant"""
	G_MAXIMUM_RADIUS = 0.03

	def __init__(self, pos=[0,0], radius_multiplier=1, color=(0,0,0), energy=0):
		self.alive = True
		self.energy = energy
		self.pos = pos
		self.radius_multiplier = radius_multiplier
		self.color = color

	def get_radius(self):
		return self.radius_multiplier * Inhabitant.G_MAXIMUM_RADIUS

	def get_color(self):
		return self.color

	def get_pos(self):
		return array(self.pos)

	def get_x(self):
		return self.pos[0]

	def get_y(self):
		return self.pos[1]

	def on_collision(self, target):
		pass

	def move(self):
		pass

	def think(self):
		pass
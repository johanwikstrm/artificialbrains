from inhabitant import Inhabitant
from creature import Creature

class Bush(Inhabitant):
	"""docstring for Bush"""
	def __init__(self, x=0, y=0, poisonous=False):
		self.poisonous = poisonous
		if poisonous:
			super(Bush, self).__init__([x,y], radius_multiplier=0.55, color=(1.0,0.0,0.0), energy=0)
		else:
			super(Bush, self).__init__([x,y], radius_multiplier=0.1, color=(0.0,1.0,0.0), energy=75)

	def think(self):
		if self.radius_multiplier < 0.4:
			self.radius_multiplier += 0.01

		#if self.color[1] < 1:
		#	self.color = (0.1,self.color[1] + 0.01, 0.1)

	def on_collision(self, target):
		if target.__class__ == Creature and not target.predator:
			if self.poisonous:
				target.alive = False
				target.cod = 'bush'
				self.alive = 0
			else:
				target.energy += self.energy
				target.consumed_energy += self.energy
				self.alive = 0

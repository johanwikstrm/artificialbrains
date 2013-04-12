import pygame,math,world,creature
from pygame.locals import *

class Renderer(object):
	"""docstring for Renderer"""
	def __init__(self, width=850, height=850):
		pygame.init()

		self.width = width
		self.height = height
		self.disp_freq = Renderer.disp_freq
		self.screen = pygame.display.set_mode((self.width,self.height), DOUBLEBUF)
		pygame.display.set_caption('Our kex')
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))
		self.screen.blit(self.background,(0,0))
		pygame.display.flip()

	def play_epoch(self, world):
		disp_freq = self.disp_freq
			
		for tick in xrange(world.nticks):
			if len(world.creatures) != 0 or len(world.predators) != 0:
				world.run_tick()
			else:
				break
			if tick % disp_freq == 0:
				self.render(world)

		self.screen.blit(self.background,(0,0))
		pygame.display.flip()

		return (world.get_creatures(), world.get_predators())

	def render(self, world):
		self.screen.blit(self.background,(0,0))

		self.render_bushes(world)
		self.render_creatures(world)

		pygame.display.flip()


	def render_bushes(self, world):
		for bush in world.get_bushes():
			pygame.draw.circle(self.screen, 
				[color * 255 for color in bush.get_color()], 
				(int(self.width * bush.pos[0]), int(self.height * bush.pos[1])),
				1 + int(bush.get_radius() * self.height),
				0)

	def render_creatures(self, world):	
		for creature in world.get_living():
			pygame.draw.line(self.screen,
				(255,255,255),
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				(int(self.width * (creature.pos[0] + creature.antennae_length * math.cos(creature.rotation * 2 * math.pi + creature.antennae_angles[0]))), 
				 int(self.height * (creature.pos[1] + -1 * creature.antennae_length * math.sin(creature.rotation * 2 * math.pi + creature.antennae_angles[0])))),
				)
			pygame.draw.line(self.screen,
				(255,255,255),
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				(int(self.width * (creature.pos[0] + creature.antennae_length * math.cos(creature.rotation * 2 * math.pi + creature.antennae_angles[1]))), 
				 int(self.height * (creature.pos[1] + -1 * creature.antennae_length * math.sin(creature.rotation * 2 * math.pi + creature.antennae_angles[1])))),
				)
			pygame.draw.circle(self.screen, 
				[color * 255 for color in creature.get_color()], 
				(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
				1 + int(creature.get_radius() * self.height),
				0)
			if creature.predator:
			 	pygame.draw.circle(self.screen, 
			 	[255,255,255], 
			 	(int(self.width * creature.pos[0]), int(self.height * creature.pos[1])),
			 	1 + int(creature.get_radius() / 3 * self.height),
			 	0)
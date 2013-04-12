import math
import numpy as np
from numpy import array

def gene2color(gene):
	color = 0.1 + (gene + 1) * 0.5
	color = color if color < 1 else 1
	color = color if color > 0 else 0
	return color

def dot(v1, v2):
	return v1.dot(v2)

vlenmap = [[math.sqrt((x/1000.0)**2 + (y/1000.0)**2) for x in xrange(1001)]  for y in xrange(1001)]

def special_vlen(v):
	x = int(abs(v[0]) * 1000)
	y = int(abs(v[1]) * 1000)
	return vlenmap[y][x]

def vlen(v):
	return np.sqrt(v.dot(v))

#import random
#def show(x,y):
#	print "x: %f y: %f" %(x,y)
#	print "svlen:", special_vlen([x,y])
#	print "vlen:", vlen(array([x,y]))
#tests = [show(random.random(),random.random()) for x in xrange(1001) for y in xrange(1001)]

def vminus(v1, v2):
	return v1-v2

def vplus(v1, v2):
	return v1+v2

def sign(f):
	if f < 0:
		return -1
	return 1

def gaussian(x, mu, sigma):
	""" definition of the guassian function"""
	y = math.exp( -1.0/2 * ((x - mu + 0.0) / (sigma + 0.000001))**2 )
	return y

def transfer(val):
	return 1.0 / (1.0 + math.exp(-1.0 * val)) * 2 - 1

def fetch_one(enumerable):
	def next_val():
		for e in enumerable:
			yield e
		raise Exception('Too many elements retrieved')

	return next_val().next


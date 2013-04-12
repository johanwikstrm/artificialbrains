import platform
if platform.python_implementation() == 'PyPy':
    import numpypy
else:
    import matplotlib.pyplot as plt 

from cPickle import Pickler,Unpickler
from collections import defaultdict
import numpy as np
import copy, argparse, sys

stats = defaultdict(list)

def add(stat,val):
	stats[stat] += [val]

def get(stat):
	return stats[stat]

def export_stats():
	return stats

def import_stats(stats_dict):
	global stats
	stats = copy.deepcopy(stats_dict)

def save_stats(save_file):
	pickler = Pickler(save_file)
	pickler.dump(stats)
	save_file.close()

def load_stats(load_file):
	unpickler = Unpickler(load_file)
	stats_to_import = unpickler.load()
	import_stats(stats_to_import)
	load_file.close()

def group_stats():
	grouped_stats = {}
	for stat in stats:
		parts = stat.split('.',1)
		if len(parts) == 2:
			if parts[0] not in grouped_stats.keys():
				grouped_stats[parts[0]] = {}

			grouped_stats[parts[0]][parts[1]] = stats[stat]

		else:
			grouped_stats[stat] = { stat: stats[stat]}

	return grouped_stats

def plot_all():
	if platform.python_implementation() == 'PyPy':
		print "Running pypy, cannot plot"
		return

	grouped_stats = group_stats()

	for stat_group in grouped_stats:
		fig = create_figure(stat_group,grouped_stats[stat_group])
		fig.show()
		dontexit = raw_input()

def save_all(save_prefix):
	grouped_stats = group_stats()

	for stat_group in grouped_stats:
		fig = create_figure(stat_group,grouped_stats[stat_group])
		print "Saving %s..." % stat_group
		fig.savefig(save_prefix + "_" + stat_group + '.png',bbox_inches=0)

def create_figure(name,stat_group):
	if platform.python_implementation() == 'PyPy':
		print "Running pypy, cannot plot"
		return

	plt.clf()

	min_y = -0.2
	max_y = 0.2

	lines = []

	for stat in stat_group:
		y_vals = stat_group[stat]
		x_vals = xrange(1,len(y_vals)+1)
		
		line, = plt.plot(x_vals, y_vals, linewidth=2.0)
		lines += [line]

		if min_y > min(y_vals)*0.90:
			min_y = min(y_vals)*0.90
		if max_y < max(y_vals)*1.1:
			max_y = max(y_vals)*1.1

	plt.axis([1, len(y_vals), min_y, max_y])
	plt.title(name)
	plt.legend(lines,stat_group.keys())
	plt.ylabel('Value')
	plt.xlabel('Generation #')
	return plt.gcf()

def main():
	parser = argparse.ArgumentParser(description='Stand alone plotting program.')
	parser.add_argument('-m', dest='mode', metavar='str', type=str, help="Run the program in the following mode. Available modes are: plot, disk")
	parser.add_argument('-l', dest='load_file', metavar='file', type=str, help="The file to load.")
	parser.add_argument('-s', dest='save_prefix', metavar='file', type=str, help="Prefix for saving images.")
	args = parser.parse_args(sys.argv[1:])
	
	if args.mode == 'plot':
		load_stats(open(args.load_file))
		plot_all()
		dontexit = raw_input()
	if args.mode == 'disk':
		load_stats(open(args.load_file))
		save_all(args.save_prefix)



if __name__ == '__main__':
	main()

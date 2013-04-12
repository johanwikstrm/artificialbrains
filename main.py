#!/usr/bin/env python
import platform
if platform.python_implementation() == 'PyPy':
    import numpypy
else:
    from renderer import Renderer

from world import World
from creature import Creature
from bush import Bush
from darwin import Darwin

import argparse, sys, cProfile, math, time

def default():
    options = {
        ('World','move'):True,
        ('World','think'):True,
        ('World','default_input'):True,
        ('World','collision'):True,
        ('World','remove_dead'):True,
        ('World','detect_creatures'):True,
        ('World','detect_bushes'):True,

        ('Darwin','save_file'): save_file or 'save.txt',

        ('Creature','World','Darwin','brain_type'): brain_type or 'BrainRBF',

        ('Darwin','NGEN'): num_gens or 0,
        ('Darwin','CXPB'):0.3,
        ('Darwin','MUTPB'):0.4,
        
        ('Creature','G_MAX_SPEED'):0.01,
        ('Creature','health'):500,
        ('Darwin','NTICKS'):2500,

        ('Darwin','NPRED'): num_preds or 0, # Must be divisible by NINDS / num_inds_per_sim and 10
        ('Darwin','NINDS'): num_inds or 120, # Must be a number divisible by 10 and by num_inds_per_sim
        ('Darwin','num_inds_per_sim'):20,

        ('Darwin','max_bush_count'): bushes_green or 0,
        ('Darwin','max_red_bush_count'): bushes_red or 0,

        ('Renderer','disp_freq'):2,
        ('Darwin','enable_multiprocessing'):True,
        ('Darwin','graphics'):False or gfx,
    }

    apply_config(options)

    darwin = Darwin()
    
    if load_file:
        darwin.load_population(open(load_file,'r'))
        darwin.load_stats(open('stats_' + load_file,'r'))

    darwin.begin_evolution()

def profile():
    cProfile.run('default()', 'stats.pstats')

def main():
    parser = argparse.ArgumentParser(description='Run the simulation.')
    parser.add_argument('-l',dest='load_file', metavar='file', type=str, help="Path to file with saved state, used to resume simulations.")
    parser.add_argument('-s',dest='save_file', metavar='file', type=str, help="Path to the file where the results will be saved.")
    parser.add_argument('-g',dest='num_gens', metavar='int', type=int, help="Number of generations to run the simulation.")
    parser.add_argument('-b',dest='brain_type', metavar='str', type=str, help="The kind of brain to use in this simulation.")
    parser.add_argument('-ni',dest='num_inds',metavar='int',type=int,help="Number of individuals")
    parser.add_argument('-np',dest='num_preds',metavar='int',type=int,help="Number of predators")
    parser.add_argument('-bg',dest='bushes_green',metavar='int',type=int,help="Number of green bushes")
    parser.add_argument('-br',dest='bushes_red',metavar='int',type=int,help="Number of red bushes")
    parser.add_argument('--profile',dest='profiling_enabled', help="Use to enable or disable generation of profiling information.", required=False, action='store_const', const=True)
    parser.add_argument('--gfx',dest='gfx', help="Used to disable multiprocessing and enable graphics", required=False, action='store_const', const=True)
    args = parser.parse_args(sys.argv[1:])

    global load_file
    global save_file
    global num_gens
    global brain_type
    global num_inds
    global num_preds
    global bushes_green
    global bushes_red
    global gfx

    load_file = None or args.load_file
    save_file = None or args.save_file
    num_gens = None or args.num_gens
    brain_type = None or args.brain_type
    num_inds = None or args.num_inds
    num_preds = None or args.num_preds
    bushes_green = None or args.bushes_green
    bushes_red = None or args.bushes_red
    gfx = None or args.gfx

    if args.profiling_enabled:
        profile()
    else:
        start = time.time()
        default()
        end = time.time()   
        print "Run-time: %f" % (0.0 + end - start)

    print "Done!"

def apply_config(config):
    for key in config.keys():
        clses = key[:-1]
        attr = key[-1]
        for cls in clses:
            if cls.istitle():
                try:
                    setattr(eval(cls),attr,config[key])
                except NameError:
                    pass

if __name__ == '__main__':
    main()

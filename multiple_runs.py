
import os

g = 300
bg = 12
br = 0 # 10
ni = 200
np = 0
#np = ni / 10
for i in range(1):	
	#for b in ['BrainLinear', 'BrainRBF']:
	for b in ['BrainRandom']:
		os.system("pypy main.py -s %s_gen%d_ind%d_pred%d_bg%d_br%d_run%d.txt -b %s -g %d -ni %d -np %d -bg %d -br %i" % (b,g,ni,np,bg,br,i,b,g,ni,np,bg,br))
		os.system("python stats.py -m disk -l stats_%s_gen%d_ind%d_pred%d_bg%d_br%d_run%d.txt -s %s_gen_%d_ind_%d_pred_%d_bg_%d_br_%d_run%d" % (b,g,ni,np,bg,br,i,b,g,ni,np,bg,br,i))
	
# Test:
# Grona buskar, inga preds x 2 
# Grona buskar, preds x 2
# Grona roda buskar x 2
# Random med alla ocksa

# Remember, can use: mv *Brain* to move all files after running
#!/bin/sh
python tools/gprof2dot.py -f pstats stats.pstats | dot -Tpng -o output.png
__author__ = 'laraib'

import csv
import time
from pylab import *
from matplotlib import *

with open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr10/chr10.uniq.test.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
#print d[0][2] # end

intervals = []

for j in range(0,len(d)):
    intervals.append((int(d[j][1]), int(d[j][2])))

def intervals2layers(si):
    layers = [[si[0]]]
    for p in si[1:]:
        for lay in layers:
            if lay[-1][-1] < p[0]:
                lay.append(p)
                break
        else:
            layers.append([p])

    return layers

si = sorted(intervals, key=lambda p: p[0])
layers = intervals2layers(si)

figsize=(8, 4)
for i, lay in enumerate(layers):
    x1, x2 = zip(*lay)
    plt.hlines([i + 1] * len(x1), x1, x2, lw=30)

plt.xlim(52280000, 69280000)
plt.ylim(0, 10)
plt.xlabel('Position along the chromosome')
plt.ylabel('Heirarchy level')
show()
print "GRAPH"
time.sleep(10)

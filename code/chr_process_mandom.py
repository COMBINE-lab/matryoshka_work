__author__ = 'laraib'

import csv
import time

outfile = open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr10/chr10.processed.txt', 'w')

with open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr10/chr10.uniq.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
#print d[0][2] # end

with open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr10/output.txt') as t:
    reader = csv.reader(t, delimiter="\t")
    prevrow = ["","",""]
    for row in reader:
        start = row[1]
        end = row[2]
        if (prevrow[1] != start) | (prevrow[2] != end):
            prevrow = row
            outfile.write('\n' + 'chr10\t' + start + '\t' + end)
        for i in range(0, len(d)):
            if ((d[i][1] == start) & (d[i][2] == end)):
                outfile.write('\t' + row[3])
        #time.sleep(5)

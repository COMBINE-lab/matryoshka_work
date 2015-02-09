__author__ = 'laraib'

import csv
import sys
import getopt

#check for overlap with part of d and if current is larger with
#80% overlap, return domain index it overlaps with, otherwise -1.
def check_overlap(d, start, end, check_point, index):
    if check_point == index:
        return -2
    check = 0
    for i in range(check_point, index+1):
        if max(start, d[i][1]) <= min(end, d[i][2]):
            val1 = min((float(end)-float(start)), (d[i][2]-d[i][1]))
            val2 = max((float(end)-float(start)), (d[i][2]-d[i][1]))
            overlap = val1/val2
        else:
            overlap = 0

        #if max(start, d[i][1]) <= min(end, d[i][2]):
        #    overlap = (float(end)-float(start))/(d[i][2]-d[i][1])
        #    if overlap > 1:
        #        overlap = (d[i][2]-d[i][1])/(float(end)-float(start))
        #else:
        #    overlap = 0

        if (overlap >= 0.8) & (overlap != 1):
            check = 1
            #if (end-start) > (d[i][2]-d[i][1]):
            #    return i
            if (end >= d[i][2]) & (start <= d[i][1]):
                return i
    if check != 1:
        return -2
    return -1

#returns number of overlaps if greater than 0
def check_overlap_basic(d, start, end, index):
    check = 0
    for i in range(0, index+1):
        if (end >= d[i][0]) & (start < d[i][0]):
            val1 = min((float(end)-float(start)), (d[i][1]-d[i][0]))
            val2 = max((float(end)-float(start)), (d[i][1]-d[i][0]))
            overlap = val1/val2
        else:
            overlap = 0
        if (overlap > 0) & (overlap != 1):
            check += 1
    if check != 1:
        return check
    return -1

def main(argv):
    coldom = [] #collapsed domains
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         infile = arg
      elif opt in ("-o", "--ofile"):
         outfile = arg

    with open(infile, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)

    chr = d[0][0]
    for i in range(0, len(d)):
        d[i][1] = int(d[i][1])
        d[i][2] = int(d[i][2])

    check_point = 0
    maxcurend = 0
    for i in range(0, len(d)):
        if len(coldom) != 0:
            if d[i][1] > maxcurend:
                check_point = i

        curstart = int(d[i][1])
        curend = int(d[i][2])

        if curend > maxcurend:
            maxcurend = curend

        pos = check_overlap(d, curstart, curend, check_point, i)
        if (pos != -1):
            coldom.append((curstart,curend))
            if pos > 0:
                if (d[pos][1],d[pos][2]) in coldom:
                    coldom.remove((d[pos][1],d[pos][2]))

    with open(outfile, 'w') as t:
        for i in range(0, len(coldom)):
            t.write(chr + '\t' + str(coldom[i][0]) + '\t' + str(coldom[i][1]) + '\t' + str(coldom[i][1] - coldom[i][0]) + '\n')
            #time.sleep(5)

    #check overlap after collapsing
    for i in range(0, len(coldom)):
        overlap = check_overlap_basic(coldom, coldom[i][0], coldom[i][1], i)
        if overlap > 0:
            #should not come here ideally
            print(coldom[i])
            #time.sleep(20)

if __name__ == "__main__":
   main(sys.argv[1:])
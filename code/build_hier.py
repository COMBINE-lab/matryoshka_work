__author__ = 'laraib'

import csv
import sys
import getopt

#check if a domain is already covering this area and return
def check_overlap_basic(d, start, end, index):
    overlap_index = -1
    max_overlap = 0
    for i in range(0, index+1):
        if max(start, d[i][1]) <= min(end, d[i][2]):
            val1 = min((float(end)-float(start)), (d[i][2]-d[i][1]))
            val2 = max((float(end)-float(start)), (d[i][2]-d[i][1]))
            overlap = val1/val2
        else:
            overlap = 0
        if (overlap > 0) & (overlap != 1):
            if (overlap > max_overlap):
                max_overlap = overlap
                overlap_index = i
    return (max_overlap, overlap_index)

def main(argv):
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

    for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         infile = arg
      elif opt in ("-o", "--ofile"):
         outfile = arg

    #collapsed heirarchies sorted in descending order on size of domains
    with open(infile, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        coldom = list(reader)

    for i in range(0, len(coldom)):
        coldom[i][1] = int(coldom[i][1])
        coldom[i][2] = int(coldom[i][2])

    heir_level = []
    heir_info = []
    outfile = open(outfile, 'w')
    outfile.write('index' + '\t' + 'chr' + '\t' + 'dom start' + '\t' + 'dom end' + '\t' +
                      'overlap %age' + '\t' + 'overlaps with' + '\t' + 'hier level' + '\n')

    for i in range(0, len(coldom)):
        overlap = check_overlap_basic(coldom, coldom[i][1], coldom[i][2], i)
        if overlap[1] != -1:
            heir_level.append(heir_level[overlap[1]] + 1)
        else:
            heir_level.append(1)
        heir_info.append(overlap)
        outfile.write(str(i) + '\t' + coldom[i][0] + '\t' + str(coldom[i][1]) + '\t' + str(coldom[i][2]) + '\t' +
                      str(heir_info[i][0]) + '\t' + str(heir_info[i][1]) + '\t' + str(heir_level[i]) + '\n')

    outfile.close()

if __name__ == "__main__":
   main(sys.argv[1:])

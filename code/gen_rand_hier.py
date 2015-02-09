__author__ = 'laraib'

#Ensure that the rank file is sorted by hierarchy level(column G) and then by domain start(column C)

import csv
import time
import random

class domain:
    def __init__(self, index, chromo, pindex, hier, start, end):
        self.myInd = int(index)
        self.parentInd = int(pindex)
        self.hierLevel = int(hier)
        self.orgStart = int(start)
        self.orgEnd = int(end)
        self.size = self.orgEnd - self.orgStart
        self.randStart = int(start)
        self.randEnd = int(end)
        self.chr = chromo
    def setRegion(self, start):
        self.randStart = start
        self.randEnd = start + self.size
        return self.size
    def printAll(self):
        return (self.chr + '\t' + str(self.randStart) +'\t' + str(self.randEnd) + '\t' + str(self.hierLevel) + '\n')

def findNondomains(pStart, pEnd, domHier, childDom):
    nondom = []
    domains = []

    for i in childDom:
        domains.append(domHier[i])

    for i in range(0, len(domains)):
        nondom.append(domains[i].orgStart-pStart)
        pStart = domains[i].orgEnd
    nondom.append(pEnd-pStart)
    return nondom

def randomizeDoms(ndSizes, domHier, childDom, stackInd, lenStart, lenEnd):
    lenScanned = lenStart

    nondomainSizes = list(ndSizes)
    random.shuffle(nondomainSizes)
    random.shuffle(childDom)

    for i in range(0, len(nondomainSizes)-1):
        nondom = nondomainSizes[i]
        lenScanned += nondom
        domSize = domHier[childDom[i]].setRegion(lenScanned)
        lenScanned += domSize
        stackInd.append(domHier[childDom[i]])
    lenScanned += nondomainSizes[len(nondomainSizes)-1]
    if lenScanned == lenEnd:
        return 1
    return 0

def nonrandomizeDoms(ndSizes, domHier, childDom, stackInd, lenStart, lenEnd):
    for i in range(0, len(ndSizes)-1):
        stackInd.append(domHier[childDom[i]])
    return 1

def getChildren(curInd, allDomains):
    childDoms = []
    for i in range(0, len(allDomains)):
        if curInd == allDomains[i].parentInd:
            childDoms.append(i)
    return childDoms

with open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr12/chr12.hier.rank.txt', 'r') as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)

domHier = []
maxHier = int(d[len(d)-1][6])
for i in range(0, maxHier):
    domHier.append([])

for i in range(1, len(d)):
    hier = int(d[i][6])
    domHier[hier-1].append(domain(d[i][0], d[i][1], d[i][5], d[i][6], d[i][2], d[i][3]))

chr_size = 135534747
stackInd = []
childDoms = getChildren(-1, domHier[0])
nondomainSizes = findNondomains(0, chr_size, domHier[0], childDoms)

randomizeDoms(nondomainSizes, domHier[0], childDoms, stackInd, 0, chr_size)

while(len(stackInd)!=0):
    curDomain = stackInd.pop()
    if curDomain.hierLevel != maxHier:
        curHier = curDomain.hierLevel
        #getchildren of current domain from curDom.hierlevel sub-array of domHier
        childDoms = getChildren(curDomain.myInd, domHier[curHier])
        #for these child domains, get sizes of the nondomains
        nondomainSizes = findNondomains(curDomain.orgStart, curDomain.orgEnd, domHier[curHier], childDoms)
        #randomize the domains in the children at this level
        randomizeDoms(nondomainSizes, domHier[curHier], childDoms, stackInd, curDomain.randStart, curDomain.randEnd)

with open('/home/laraib/Desktop/COMBINE lab work/armatus-master/data/IMR90/chr12/chr12.hier.rand.txt', 'w') as t:
    for i in range(0, maxHier):
        for j in range(0, len(domHier[i])):
            t.write(domHier[i][j].printAll())

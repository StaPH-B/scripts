#!/usr/bin/env python
#This script takes in an ordered file and then returns a pairwise matrix based on that order.
#Usage (must be run from directory above lyveset): ordered_pairwise_matrix_generator.py /path/to/ordered/file
#Last updated: 05/10/18
import argparse, sys, os
cwd = os.getcwd()
parser = argparse.ArgumentParser()
pairwiseFile = str(cwd)+'/lyveset/msa/out.pairwise.tsv'
parser.add_argument('-p', dest='pairwise', help='a pairwise list of all possible combinations in pairwise matrix.', default=pairwiseFile)
parser.add_argument('-i', dest='inputFile', help='input file; text file as an ordered list of the isolates.')
parser.add_argument('-pm', dest='pairwiseMatrix', help='a pairwise matrix of all snps between isolates of interest.')
args = parser.parse_args()

#Create a pairwise dictionary with all values possible, and create a list of the isolates
pairwiseDict = {}
isolates = []
f = open(args.pairwise, 'r')
flines  = f.readlines()
for line in flines:
    print line
    line = line.strip('\n')
    linesplit = line.split('\t')
    pairwiseDict[linesplit[0], linesplit[1]] = linesplit[2]
    pairwiseDict[linesplit[1], linesplit[0]] = linesplit[2]
    if not linesplit[0] in isolates:
        isolates.append(linesplit[0])
    if not linesplit[1] in isolates:
        isolates.append(linesplit[1])
f.close()

#Take in the ordered list created by the user and create a list object
orderedList = []
g = open(args.inputFile, 'r')
glines = g.readlines()
for line in glines:
    line = line.strip('\n')
    if str(line)[0] == "#":
        pass
    else:
        orderedList.append(line)
g.close()

#This is to make sure that if the names aren't exactly the same in the ordered file
#(eg. doesn't include ".cleaned"), they will still work
newOrderedList = []
for item in orderedList:
    original = 1
    for isolate in isolates:
        if str(item) in str(isolate):
            newOrderedList.append(isolate)
            original = 0
        elif str(isolate) in str(item):
            newOrderedList.append(isolate)
            original = 0
        else:
            continue
    if original==1:
        newOrderedList.append(item)

#Open the output file and write the first line
z=open("out.pairwiseMatrix.sorted.tsv", 'w')
z.write(".")
for item in newOrderedList:
    z.write('\t')
    z.write(str(item))
z.write('\n')

#Write the matrix using the ordered pairs dictionary
for item1 in newOrderedList:
    z.write(str(item1))
    for item2 in newOrderedList:
        if item1 == item2:
            z.write('\t')
            z.write("-")
        else:
            z.write('\t')
            z.write(str(pairwiseDict[item1, item2]))
    z.write('\n')
z.close()
print "Matrix has been created in current directory as 'out.pairwiseMatrix.sorted.tsv.'"

import numpy as np
import csv
import utility
from learnAlg import *

def constraintBN(filename, location, sample_size = 100, iteration = 1, alpha = 0.5):
    # left -> right
    edge = {}
    print "sample_size: {}, iterations: {}, alpha: {}".format(sample_size, iteration, alpha)
    for i in range(iteration):
        print "iteration {}".format(i)
        path = location + filename
        #clean_path = location + filename.split(".")[0] + "-num.csv"
        # Reformat data and replace string, size = sample_size
        data, field = utility.reformat(path, size = sample_size)
        if i == 0:
            utility.printAttr(field)
        data = np.array(data, np.int32)
        #data = np.genfromtxt(clean_path, dtype='int32', delimiter=',')
        # 1. Find Markov Blankets
        mb = gs(data, alpha = alpha)
        mb = check_symmetric(mb)
        # 2. learning neighbors
        nb = learnNb(data, mb, alpha = alpha)
        nb = check_symmetric(nb)
        # 3. learning directions
        arc = learnDir(data, nb, alpha = alpha)
        # majority vote
        for left in arc.keys():
            right = arc[left]
            if left not in edge.keys():
                edge[left] = {}
            for r in right:
                if r not in edge[left].keys():
                    edge[left][r] = 1
                else:
                    edge[left][r] += 1
    printEdge(edge, itr = iteration)
    return edge

def printEdge(edge, itr, threshold = 0.5):
    for e in edge:
        right = edge[e]
        for r in right:
            if edge[e][r] > threshold*itr:
                print "{} -> {} ({})".format(e, r, edge[e][r])

if __name__ == '__main__':
    filename = '500_Cities__Local_Data_for_Better_Health__2017_release.csv'
    location = '/Users/scarlet/Documents/holocleandiscoverFDs/datasets/'
    edges = constraintBN(filename, location)
    #print edges
    
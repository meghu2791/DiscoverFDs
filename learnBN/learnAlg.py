import numpy as np
from scipy import stats
from copy import copy
from utility import *

'''
learn Markov Blanket Using GS
'''
def gs(data, alpha):
    # number of attributes
    n_attr = data.shape[1]
    # number of records
    n_rec = data.shape[0]
    col_index = range(n_attr)
    # init empty blanket container for each attri
    blanket = dict([(i,[]) for i in range(n_attr)])
    for X in col_index:
        # step 1: init blanket for attri
        S = []
        # step2: GROWING phase
        for Y in col_index:
            # exists Y not belonging to X nor S
            if X != Y and Y not in S:
                columns = (X,Y) + tuple(S)
                if not are_independent(data[:,columns]):
                    S.append(Y)
        # step3: SHRINKING phase
        for Y in S:
            # test if Y == X 
            if X != Y:
                new_S = copy(S)
                new_S.remove(Y)
                columns = (X,Y) + tuple(new_S)
                # Y indep of X given S - Y, S = S - Y
                if are_independent(data[:,columns]):
                    S = new_S
        # save to blanket
        blanket[X] = S
    return blanket

'''
learn neighbours
'''
def learnNb(data, mb, alpha):
    nb = {}
    # N(x) is subset of B(x)
    for x in range(data.shape[1]):
        nb[x] = []
        for y in range(data.shape[1]):
            if x in mb[y]:
                space = copy(mb[y]).remove(x)
                noset = True
                if space != None:
                    subset = find_subset(space)
                    # print "subset for {}".format(x)
                    # print subset
                    for s in subset.values():
                        columns = (x,y,s)
                        if are_independent(data[:,columns]):
                            noset = False
                            break
                # test empty s
                columns = (x,y)
                if are_independent(data[:,columns]):
                    noset = False
                if noset:
                    nb[x].append(y)
                    # place an undirected edge beteewn x and y
                    #print "{} and {} has an edge".format(x, y)
    return nb

'''
learn arc directions
'''
def learnDir(data, nb, alpha):
    leftToRight = {}
    # find V-structure
    for x in nb.keys():
        leftToRight[x] = []
        for y in range(x+1, data.shape[1]):
            # find non-adjacent x,y
            if y in nb[x]:
                continue
            # find their common neighbor
            commonNb = list(set(nb[x]).intersection(nb[y]))
            for s in commonNb:
                # check if x and y are independent given common neighbour belongs
                columns = (x,y,s)
                if not are_independent(data[:,columns]):
                    if s not in leftToRight[x]:
                        leftToRight[x].append(s)
                    if y not in leftToRight.keys():
                        leftToRight[y] = []
                    if s not in leftToRight[y]:
                        leftToRight[y].append(s)
                    #print "{} -> {} <- {}".format(x, s, y)
    # recursively applying two rules util converge
    last = {}
    while last != leftToRight:
        last = copy(leftToRight)
        for x in nb.keys():
            for y in nb.keys():
                # case1: adjacent
                if y in nb[x]:
                    # find undirected edges
                    if y in leftToRight[x] or x in leftToRight[y]:
                        continue
                    # if existing a directed path from x to y, set x -> y
                    if hasDirectedPath(x,y,leftToRight):
                        if y not in leftToRight[x]:
                            leftToRight[x].append(y)
                        #print "{} -> {}".format(x, y)

                # case2: non-adjacent
                # if existing s that x -> s and s - y. set s -> y
                else:
                    for s in leftToRight[x]:
                        if s in nb[y]:
                            # not s <- y
                            if y not in leftToRight[s] and s not in leftToRight[y]:
                                leftToRight[s].append(y)
                            #print "{} -> {}".format(s, y)
    return leftToRight


def hasDirectedPath(x, y, leftToRight):
    if leftToRight[x] == None:
        return False
    if y in leftToRight[x]:
        return True
    else:
        for i in leftToRight[x]:
            if hasDirectedPath(i, y, leftToRight):
                return True

'''
check symmetric for mb or nb
'''
def check_symmetric(mb):
    new_mb = dict(mb)
    attr = mb.keys()
    for x in attr:
        for i in mb[x]:
            if x not in mb[i]:
                new_mb[x].remove(i)
    return new_mb



import numpy as np
import math
from scipy.spatial.distance import euclidean
from pandas import DataFrame
from scipy import stats
from copy import copy
from utility import *

ZERO = 0.0000000001
SQRT2 = np.sqrt(2)

def findFD_Distance(data, bins):
    n_attr = data.shape[1]
    n_rec = data.shape[0]
    col_index = range(n_attr)

    # dic of edges: {left:{right:score}}
    edges = np.zeros(((n_attr),(n_attr)))

    for X in col_index:
        for Y in range(X+1, n_attr):
            bx = bins[X]
            by = bins[Y]
            # if by == 1:
            #     edges[X][Y] = 1
            #     edges[Y][X] = 0
            #     continue
            # elif bx == 1:
            #     edges[Y][X] = 1
            #     edges[X][Y] = 0
            #     continue
            if by == 1 or bx == 1:
                edges[X][Y] = 0
                edges[Y][X] = 0
                continue
            hist,_ = np.histogramdd(data[:, (X,Y)], bins = [bx,by])
            pxy = hist / n_rec
            # x -> y: H(Y|X) = 0, max H(Y|X) is H(Y)
            # y -> x: H(X|Y) = 0
            edges[X][Y] = calDistance(pxy, n_rec, bx, by)

            edges[Y][X] = calDistance(pxy, n_rec, bx, by, reverse = True)
            
    return edges

def calDistance(pxy, n, bx, by, reverse = False):

    if reverse:
        pxy = np.transpose(pxy)
        tmp = bx
        bx = by
        by = tmp

    # create a closet distribution without violation
    q = fdModel(pxy,n,bx,by)
    dis = HelligerDistance(pxy,q,bx*by)
    # normalize distance: [0, sqrt(bx*by/2)]
    return 1 - dis

def fdModel(pxy,n,bx,by):
    # model: given each x, only the max index = 1, all the other are 0
    maxpx = np.argmax(pxy,1)
    model = np.zeros((bx,by))
    px = np.sum(pxy,1)
    for i in range(bx):
        model[i][maxpx[i]] = 1 * px[i]
    return model

def HelligerDistance(p,q,shape):
    return euclidean(np.reshape(np.sqrt(p), shape), np.reshape(np.sqrt(q), shape)) / SQRT2

# def calKL_fd(pxy, n, bx, by, reverse = False):
#     kl_pq = 0
#     if reverse:
#         pxy = np.transpose(pxy)
#         tmp = bx
#         bx = by
#         by = tmp

#     px = np.sum(pxy,1)
#     # a list of max frequency given x = xi
#     maxpx = np.argmax(pxy,1)

#     for i in range(bx):
#         pxi = px[i]
#         index = maxpx[i]
#         for j in range(by):
#             if j == index:
#                 # dl = pxy * log(pxy / qxy) =  pxy * log(pxy / qy_x * qxi)
#                 # = pxy * log(pxy / qy_x * pxi)
#                 kl_pq += KL(pxy[i][j], pxi * 1)
#                 kl_qp += KL(pxi * 1, pxy[i][j])
#             else:
#                 kl_pq += KL(pxy[i][j], pxi * 0)
#                 kl_qp += KL(pxi * 0, pxy[i][j])

#     return kl_pq, kl_qp

# def KL(p,q):
#     return math.log((p + ZERO) / (q + ZERO)) * p

def findFD_entropy(data, bins):

    n_attr = data.shape[1]
    n_rec = data.shape[0]
    col_index = range(n_attr)

    # dic of edges: {left:{right:score}}
    edges = np.zeros(((n_attr),(n_attr)))

    for X in col_index:
        for Y in range(X+1, n_attr):
            bx = bins[X]
            by = bins[Y]
            # if by == 1:
            #     edges[X][Y] = 1
            #     edges[Y][X] = 0
            #     continue
            # elif bx == 1:
            #     edges[Y][X] = 1
            #     edges[X][Y] = 0
            #     continue
            if by == 1 or bx == 1:
                edges[X][Y] = 0
                edges[Y][X] = 0
                continue
            hist,_ = np.histogramdd(data[:, (X,Y)], bins = [bx,by])
            pxy = hist / n_rec
            # x -> y: H(Y|X) = 0, max H(Y|X) is H(Y)
            # y -> x: H(X|Y) = 0
            hy_x, hx_y, hy, hx = calEntropy(pxy, n_rec, bx, by)
            # fd score in range [0,1], when score = 1, fd holds
            edges[X][Y] = (hy - hy_x) / hy
            edges[Y][X] = (hx - hx_y) / hx
            
    return edges

def findTrueFD(data, bins):
    n_attr = data.shape[1]
    n_rec = data.shape[0]
    col_index = range(n_attr)

    # dic of edges: {left:{right:score}}
    edges = np.zeros(((n_attr + 1),(n_attr + 1)))

    for X in col_index:
        for Y in range(X+1, n_attr):
            bx = bins[X]
            by = bins[Y]
            if by == 1 or bx == 1:
                edges[X][Y] = 0
                edges[Y][X] = 0
                continue
            hist,_ = np.histogramdd(data[:, (X,Y)], bins = [bx,by])
            # test X -> Y: 
            edges[X][Y] = calSupport(hist, n_rec, bx)
            # test Y -> X:
            edges[Y][X] = calSupport(hist, n_rec, by, x = False)

    return edges

#def findPairFD(data, bins, a1):
#
#    n_attr = data.shape[1]
#    n_rec = data.shape[0]
#    col_index = range(n_attr)
#
#    # dic of edges: {left:{right:score}}
#    edges = np.zeros(((n_attr + 1),(n_attr + 1)))
#
#    for X in col_index:
#        for Y in range(X+1, n_attr):
#            bx = bins[X]
#            by = bins[Y]
#            # if by == 1:
#            #     edges[X][Y] = 1
#            #     edges[Y][X] = 0
#            #     continue
#            # elif bx == 1:
#            #     edges[Y][X] = 1
#            #     edges[X][Y] = 0
#            #     continue
#            if by == 1 or bx == 1:
#                edges[X][Y] = 0
#                edges[Y][X] = 0
#                continue
#            hist,_ = np.histogramdd(data[:, (X,Y)], bins = [bx,by])
#            pxy = hist / n_rec
#            # test X -> Y:
#            edges[X][Y] = calSupport(hist, n_rec, bx)
#            # test Y -> X:
#            edges[Y][X] = calSupport(hist, n_rec, by, x = False)
#            # optimize: prune: if x -> y, y -> z, then x -> z
#    return edges

def calEntropy(pxy, n, bx, by):
    hxy = 0
    hx = 0
    hy = 0
    px = np.sum(pxy,1)
    py = np.sum(pxy,0)
    pxy += 0.0000000001
    px += 0.0000000001
    py += 0.0000000001
    for i in range(bx):
        pxi = px[i]
        for j in range(by):
            pyj = py[j]
            hxy += pxy[i][j] * math.log(pxy[i][j])
            hx += pxy[i][j] * math.log(pxi)
            hy += pxy[i][j] * math.log(pyj)
    hxy = -hxy
    hx = -hx
    hy = -hy
    hy_x = hxy - hx
    hx_y = hxy - hy
    return hy_x, hx_y, hy, hx

            
def calSupport(hist, n_rec, bx, x = True):
    hasFD = False
    for i in range(bx):
        # P(Y) density function given X=i
        if x:
            y_xi = hist[i,:]
        else:
            y_xi = hist[:,i]
        nxi = np.sum(y_xi)
        if (max(y_xi) == nxi):
            hasFD = True
        else:
            return False
    return hasFD

def helper(hist, n_rec, bx, x = True):
    hasFD = False
    for i in range(bx):
        # P(Y) density function given X=i
        if x:
            y_xi = hist[i,:]
        else:
            y_xi = hist[:,i]
        nxi = np.sum(y_xi)
        # if (max(y_xi) != nxi):
        #     print (max(y_xi))
        #     print(nxi)
        #     print(i)
        #     print(np.argmax(y_xi))
        #     print(y_xi[np.argmax(y_xi)])



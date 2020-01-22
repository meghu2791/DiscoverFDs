import numpy as np
from scipy import stats
from copy import copy
import csv
import math


def are_independent(data, alpha = 0.05):
    pval = indep_test(data)
    if pval < alpha:
        return True
    else:
        return False

'''
Independent tests:
@param test: perform chi-square test
For data = [X,Y]
- calculate joint prob
- calculate marginal prob
- cross product of marginal X and marginal Y
- calculte mutaual info I(X;Y): how much one random variables tells us about another
'''
def indep_test(data, test=True):
    bins = unique_bins(data)
    n_row = data.shape[0]
    if len(bins) == 2:
        # PAGE 788-789
        # frequency counts
        hist,_ = np.histogramdd(data, bins=bins[0:2]) 
        # joint probability distribution over X,Y,(Z)
        Pxy = hist / data.shape[0] 
        # marginal: axis 0: combine rows/across X; axis 1: combine cols/across Y
        Px = np.sum(Pxy, axis = 1) # P(X,Z)
        Py = np.sum(Pxy, axis = 0) # P(Y,Z) 
        # avoid division by zero
        Px += 1e-7
        Py += 1e-7
        # deviance using chi-square
        chi = 0
        for i in range(bins[0]):
            for j in range(bins[1]):
                chi += n_row * math.pow(Pxy[i][j] - Px[i] * Py[j], 2) / Px[i] * Py[j]
        dof = (bins[0] - 1) * (bins[1] - 1)
        p_val = 2*stats.chi2.pdf(chi, dof) # 2* for one tail
        return round(p_val,4)
    
#         # caculate deviance measure using emprical mutual information I(X;Y)
#         MI = np.sum(Pxy * np.log(Pxy / (PxPy)))
    else:
        # PAGE 790, condition on Z
        # CHECK FOR > 3 COLUMNS -> concatenate Z into one column
        if len(bins) > 3:
            data = data.astype('str')
            ncols = len(bins)
            for i in range(len(data)):
                data[i,2] = ''.join(data[i,2:ncols])
            data = data.astype('int')[:,0:3]

        bins = unique_bins(data)
        hist,_ = np.histogramdd(data, bins=bins)

        # joint probability distribution over X,Y,Z
        Pxyz = hist / n_row
        Pz = np.sum(Pxyz, axis = (0,1)) # P(Z)
        Pxz = np.sum(Pxyz, axis = 1) # P(X,Z)
        Pyz = np.sum(Pxyz, axis = 0) # P(Y,Z)   

        Pxy_z = Pxyz / (Pz+1e-7) # P(X,Y | Z) = P(X,Y,Z) / P(Z)
        Px_z = Pxz / (Pz+1e-7) # P(X | Z) = P(X,Z) / P(Z)   
        Py_z = Pyz / (Pz+1e-7) # P(Y | Z) = P(Y,Z) / P(Z)

        Px_y_z = np.empty((Pxy_z.shape)) # P(X|Z)P(Y|Z)
        
        # avoid division by zero
        Pz += 1e-7
        
        # (M[x,y,z] - M*P(z)P(x|z)P(y|z))^2 / M * P(z)P(x|z)P(y|z)
        chi = 0
        for i in range(bins[0]):
            for j in range(bins[1]):
                for k in range(bins[2]):
                    Px_y_z[i][j][k] = Px_z[i][k]*Py_z[j][k] + 1e-7
                    chi += n_row * math.pow((Pxyz[i][j][k] - Pz[k] * Px_y_z[i][j][k]), 2) / (Pz[k] * Px_y_z[i][j][k])
        dof = (bins[0] - 1) * (bins[1] - 1) * bins[2]
        p_val = 2*stats.chi2.pdf(chi, dof) # 2* for one tail
        
        return round(p_val,4)
        
#         # emprical mutual information
#         MI = np.sum(Pxyz * np.log(Pxy_z / (Px_y_z)))
#         return round(MI,4)


"""
Get the unique values for each column in a dataset.
"""
def unique_bins(data):

    bins = np.empty(len(data.T), dtype=np.int32)
    i = 0
    for col in data.T:
        bins[i] = len(np.unique(col))
        i+=1
    return bins

"""
Takes a dataset of strings and returns the
integer mapping of the string values.
It might be useful to return a dictionary of the
string values so that they can be mapped back in
the actual BayesNet object when necessary.
"""
def replace_str(data, return_dic = False):
    i = 0
    value_dic = {}
    for col in range(len(data[0])):
        unique = {}
        index = 0
        t = 0
        for row in data:
            #print "--{}--".format(row)
            if row[col] not in unique.keys():
                unique[row[col]] = index
                row[col] = index
                index+=1
            else:
                row[col] = unique[row[col]]
        value_dic[col] = unique
    if return_dic:
        return data, value_dic
    else:
        return data

def reformat(path, clean_path = "", size = 1000):
    with open(path) as csvfile:
        raw = csvfile.readlines()
        fieldnames = raw[0].strip('\n').split(",")
    raw = raw[1:]
    sample = np.random.choice(len(raw), size)
    sample = sample.tolist()
    split_raw = []
    for i in sample:
        row = raw[i].split(",")
        split_raw.append(row)
    numeric_raw = replace_str(split_raw)
    # with open(clean_path, 'wb') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',')
    #     for row in numeric_raw:
    #         writer.writerow(row)
    return numeric_raw, fieldnames

def find_subset(col, limit = 0):
    n = len(col)
    if limit == 0:
        limit = n
    if limit > n:
        limit = n  
    subset = {}
    if limit == 1:
        subset[1] = []
        for i in col:
            subset[1].append(i)
    elif limit == 2:
        subset[1] = []
        subset[2] = []
        t = 0
        for i in col:
            t += 1
            subset[1].append(i)
            for j in col[t:]:
                subset[2].append([i,j])
    elif limit >= 3:
        subset = find_subset(col, limit-1)
        subset[limit] = []
        sub = subset[limit-1]
        t = 0
        for k in sub:
            i = col.index(k[-1])
            for s in col[i+1:n]:
                if s not in k and s!= None:
                    t = copy(k)
                    t.append(s)
                    subset[limit].append(t)
    return subset


def printAttr(fieldnames):
    print "Attributes - Index"
    index = 0
    for f in fieldnames:
        print "{} - {}".format(f, index)
        index += 1

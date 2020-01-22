import numpy as np
from scipy import stats
from copy import copy
import csv
import math
import pandas as pd


"""
Get the unique values for each column in a dataset.
- value_dic = {col_num:{row_value:index}} 
"""
def unique_bins(value_dic):
    # value_dic = {col_num:{row_value:index}} 
    bins = []
    for i in value_dic.keys():
        bins.append(len(value_dic[i].keys()))
    return bins

"""
Takes a dataset of strings and returns the
integer mapping of the string values.
- return_dic: True - return value_dic
- value_dic a dictionary of the string values 
mapped with numeric value (index)
format: value_dic = {col_num:{row_value:index}} 
"""
def replace_str(data, return_dic = False):
    i = 0
    value_dic = {}
    for col in range(len(data[0])):
        unique = {}
        index = 0
        t = 0
        for row in data:
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

'''
Read and preprocess the data
- read
- obtain column name
- sample
- replace string with numeric value
- optional: write preprocessed data to file
'''
def reformat(raw, size, write_num = False, clean_path = "processed.csv"):
    
    # random sampling
    split_raw = []
    if size > 0:
        sample = np.random.choice(len(raw), size)
        sample = sample.tolist()
    else:
        # when not take sample
        sample = range(len(raw))
    for i in sample:
        row = raw[i].split(",")
        row = map(lambda x: "empty" if x == '""' else x, row)
        split_raw.append(row)

    # preprocessing: replace string with numeric value
    numeric_raw, value_dic = replace_str(split_raw, return_dic = True)
    bins = unique_bins(value_dic)

    # write data after replacing strs if needed
    if write_num:
        with open(clean_path, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in numeric_raw:
                writer.writerow(row)

    return numeric_raw, value_dic, bins


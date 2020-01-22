import numpy as np
import csv
import utility
import time
import argparse
import math
import scipy
import json
import sys, os
from learnAlg import *
from Operation import *


if __name__ == '__main__':

    # sample usage: python main.py --i 5 --s 0.3 --t 0.88 --e --haskey

    parser = argparse.ArgumentParser(description='Specify sample_size and iteration')
    parser.add_argument('--i', type = int, nargs='*', help='<Required> iterations list', required=True)
    parser.add_argument('--s', type = float, nargs='+', help='<Required> sample', required=True)
    parser.add_argument('--t', type = float, nargs='+', help='<Required> threshold', required=True)
    # parser.add_argument('-a1', type=float, default=0.6, help='threshold for first filter')
    parser.add_argument('--silent', action = 'store_true', help='output cmd message to file')
    # parser.add_argument('--dc', action = 'store_true', help='output dc file')
    parser.add_argument('--e', action = 'store_true', help='evaluate accuracy')
    # parser.add_argument('--entropy', action = 'store_true', help='using entropy')
    parser.add_argument('-dataset', type=str, default='inputDatabase.csv',help='input dataset')
    parser.add_argument('-correct', type=str, default='hospital_correct.csv',help='dataset for evaluation')
    parser.add_argument('--haskey', action = 'store_true', help='no need to generate key')
    args = parser.parse_args()
    print("iterations: ")
    print(args.i)
    print("sample ratios: ")
    print(args.s)
    print("thresholds: ")
    print(args.t)

    ID = "0313"
    read_loc = "../datasets/"
    write_loc = "./output"

    o = Operation(ID, read_loc, write_loc, args.dataset, args.correct, 
        evaluate = args.e, haskey = args.haskey, silent = args.silent)

    if len(args.i) == 1 and len(args.s) == 1 and len(args.t) == 1:
        o.run_single(args.s, args.i, args.t)
    else:
        o.run_batch(args.s, args.i, args.t)







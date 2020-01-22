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
# from Operation import *

class Session(object):

    def __init__(self, ID, dataname, dataset, field, write_loc, mode = "normal", test = "fd"):

        self.ID = ID
        self.inputName = dataname
        self.dataset = dataset
        self.field = field
        self.write_loc = write_loc
        # mode "key": generate key for ground truth input
        # mode "normal": find constraints
        self.mode = mode
        # type of constraints to find, e.g. "fd"
        self.test = test
        self.ready = False
        self.tuples = len(self.dataset)
        self.start_time = time.time()
        self.outEv = None
        self.outDC = None
        self.DC = False
        self.result = None

    def config(self, sample, itr, threshold, silent, ev, key):
        self.sample = sample
        self.iteration = itr
        self.threshold = threshold
        self.evaluate = ev
        self.silent = silent
        self.key = key
        self.ready = True
        self.initialization()

    # configuration for finding key based on ground truth
    def config_test(self):
        self.silent = True
        self.sample = 0
        self.iteration = 1
        self.threshold = 1
        self.evaluate = False
        self.ready = True
        self.initialization()
        print("...find output of contraints from ground truth at {}".format(self.log))
        return self.result

    def initialization(self):
        self.orig_stdout = sys.stdout
        if self.evaluate or self.silent:
            self.initloc()
        if self.silent:
            self.initlog()
        if self.evaluate:
            self.initOutputEv()
        if self.DC:
            self.initOutputDC()
        # print info of the data
        print("dataset: {} tuples, {} attributes".format(self.tuples, len(self.field)))
        self.run()

    def initloc(self):
        directory = r"{}".format(self.write_loc)
        if not os.path.exists(directory):
            os.makedirs(directory)
        idfolder = r"{}/{}".format(self.write_loc,self.ID)
        if not os.path.exists(idfolder):
            os.makedirs(idfolder)
        self.write_loc = idfolder

    def initlog(self):
        directory = r"{}/log".format(self.write_loc)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if self.mode == "normal":
            self.log = open(directory + '/{}_s_{}_i_{}_t_{}.txt'.format(self.ID, self.sample,
             self.iteration, self.threshold), 'w+')
        else:
            self.log = open(directory + '/{}_key.txt'.format(self.ID),'w+')
        sys.stdout = self.log

    def initOutputEv(self):
        self.outEv = open(self.write_loc + '/{}-evaluation.txt'.format(self.inputName.split(".")[0]), 'a+')

    def initOutputDC(self):
        directory = r"{}/denial_constraints".format(self.write_loc)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.outDC = open(directory + '/{}_s_{}_i_{}_t_{}.txt'.format(self.ID, self.sample,
             self.iteration, self.threshold), 'w+')

    def run(self):
        if self.test == "fd":
            semiresult = self.findFD()
        self.dtime = time.time() - self.start_time
        self.summarize(semiresult)
        if self.evaluate:
            self.evaluateResult()
        sys.stdout = self.orig_stdout

    def findFD(self):

        sample_size = int(self.sample*self.tuples)

        print ("sample: {}, iterations: {}\n".format(sample_size, self.iteration))

        allmat = {}

        for i in range(self.iteration):

            # Reformat data and replace string, size = sample_size
            if self.mode == "key":
                data, value_dic, bins = utility.reformat(self.dataset, 0)
                data = np.array(data, np.int32)
                #print data
                edges = findTrueFD(data, bins)
            else:
                #print "iteration {}".format(i)
                data, value_dic, bins = utility.reformat(self.dataset, sample_size)
                data = np.array(data, np.int32)
                #edges = findFD_entropy(data, bins)
                edges = findFD_Distance(data, bins)

            for j in range(len(edges[0, :])):
                if j not in allmat.keys():
                    allmat[j] = {}
                for k in range(len(edges[0, :])):
                    if k not in allmat[j].keys():
                        allmat[j][k] = list()
                    allmat[j][k].append(edges[j][k])
    
        return allmat

    def evaluateResult(self):
        count = self.result['count']
        TP = 0

        for row in self.result.keys():
            if row == "count" or self.result[row] == None:
                continue

            for col in self.result[row].keys():

                if row in self.key.keys():
                    if col in self.key[row].keys():
                        TP += 1

        FP = count - TP
        FN = self.key['count'] - TP
        total = scipy.misc.comb(len(self.result.keys()), 2, exact = False)
        TN = total - TP - FN - FP
        if (TP + FP) != 0 and TP + FN != 0:
            precision = TP / float((TP + FP))
            recall = TP / float((TP + FN))
        else:
            precision = 0
            recall = 0
        print("Evaluation Result: ")
        print("Precision: {} Recall: {}".format(precision,recall))
        # write evaluations
        self.outEv.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(self.ID, 
            self.inputName, self.tuples, self.sample, self.iteration, self.threshold, 
            self.dtime, count, TP, TN, FP, FN, precision, recall) )

    def summarize(self, edge):
        reformat = {}
        count = 0
        for row in range(len(edge.keys())):
            for col in range(row + 1, len(edge.keys())):
                # row -> col
                a = np.median(edge[row][col])
                b = np.median(edge[col][row])
                if a >= self.threshold:
                    if self.field[row] not in reformat.keys():
                        reformat[self.field[row]] = {}
                    reformat[self.field[row]][self.field[col]] = a
                    count += 1
                if b >= self.threshold:
                    if self.field[col] not in reformat.keys():
                        reformat[self.field[col]] = {}
                    reformat[self.field[col]][self.field[row]] = b
                    count += 1

        reformat['count'] = count
        self.result = reformat
        #print(self.result)
        self.printDC()
        self.outputFile()
        print("total count: {}\n".format(count))

    def printDC(self):
        for row in self.result.keys():
            if row == "count" or self.result[row] == None:
                continue

            # format output
            if self.test == "fd":
                string = "{} ->".format(row)

            for col in self.result[row].keys():

                # format output
                if self.test == "fd":
                    string += " {} ({}),".format(col, self.result[row][col])

            print("{}\n".format(string))
    
    def outputFile(self):
        fpipe = open("output.csv", "w")
        for row in self.result.keys():
            if row == "count" or self.result[row] == None:
                continue
            if self.test == "fd":
                for col in self.result[row].keys():
                    fpipe.write(row + ',' + col + '\n')





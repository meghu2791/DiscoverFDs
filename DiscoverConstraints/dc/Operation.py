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
from Session import *

class Operation(object):

    def __init__(self, ID, read_loc, write_loc, inputName, 
        evName, evaluate = False, haskey = False, silent = False):
        self.ID = ID
        self.read_loc = read_loc
        self.write_loc = write_loc
        # name of input data
        self.inputName = inputName
        # name of ground truth
        self.evName = evName
        # evaluate the accuracy or not
        self.evaluate = evaluate
        # has key json file or not
        self.haskey = haskey
        self.key = None
        # mute output cmd message and save it to file
        self.silent = silent
        self.loadData()

    def loadData(self):
        print("...Loading data")
        # input data
        path = self.read_loc + self.inputName
        # read file
        with open(path) as csvfile:
            raw = csvfile.readlines()
            fieldnames = raw[0].strip('\n').split(",")
        # get column name
        fieldnames[-1] = fieldnames[-1].replace('\r','')
        self.inputData = raw[1:len(raw)-1]
        self.field = fieldnames

        # if evaluate == true and no key present, 
        # need to generate fds for ground truth
        if not self.haskey and self.evaluate:
            print("...Loading ground truth")
            path2 = self.read_loc + self.evName
            # read file
            with open(path2) as csvfile:
                raw2 = csvfile.readlines()
                fieldnames = raw2[0].strip('\n').split(",")
            # get column name
            fieldnames[-1] = fieldnames[-1].replace('\r','')
            self.evData = raw2[1:len(raw2)-1]
            self.evField = fieldnames

    def run_single(self, sample, iterations, threshold):
        if (not self.haskey) and self.evaluate:
            self.generate_key()
        if self.haskey:
            self.load_key()
        print("...Finding fds ...")
        session = Session(self.ID, self.inputName, self.inputData, 
                        self.field, self.write_loc, mode = "normal")
        session.config(sample[0], iterations[0], threshold[0], self.silent, self.evaluate, self.key)

    def run_batch(self, sample, iterations, threshold):
        if (not self.haskey) and self.evaluate:
            self.generate_key()
        if self.haskey:
            self.load_key()
        print("...Finding fds ...")
        for s in sample:
            for i in iterations:
                for t in threshold:
                    session = Session(self.ID, self.inputName, self.inputData, 
                        self.field, self.write_loc, mode = "normal")
                    session.config(s, i, t, self.silent, self.evaluate, self.key)

    def generate_key(self):
        print("...Genertating key ...")
        session = Session(self.ID, self.evName, self.evData, self.evField, self.write_loc, mode = "key")
        self.key = session.config_test()
        # save the key
        keyName = self.read_loc + "key-{}.json".format(self.inputName.split(".")[0])
        keyfile = open(keyName,"w+")
        keyfile.write(json.dumps(self.key))
        print(self.key)

    def load_key(self):
        keyName = self.read_loc + "key-{}.json".format(self.inputName.split(".")[0])
        keyfile = open(keyName,"r")
        self.key = json.load(keyfile)
        print("...json file of key at {}".format(keyfile))

import pandas as pd
import numpy as np
from core.learnMRFs import learnMRF
#from core.learnBNs import learnBN
import os

class Profiler(object):
    # __metaclass__ = ABCMeta
    def __init__(self, data):
        self.df = data.toPandas()

    def showData(self):
        print(self.df.head())

    def preprocessing(self):
        self.df = self.df.dropna(axis=1, how='any')

    def findConstraints(self, options):
        if options == 1:
            mrf = learnMRF(self.df)
            mrf.createMRFs()
        elif options == 2:
            #self.createBNs()
            # bn.createBNs()
            print "TDOD"
        elif options == 3:
            #self.entropy()
            print "TODO"

    def helperFunction(self):
        print("Option 1: MRFs \nOption 2: BayesianNets \nOption 3: entropy based FD discovery \n")
    
    def load_denialConstraints(self, fname, option):
        if option == 1:
            fname = open(fname, 'w')
            self.dfFD = pd.read_csv("output.csv", encoding='utf8', dtype=object)
            col1 = []
            col2 = []
            col1 = self.dfFD[self.dfFD.columns[0]].tolist()
            col2 = self.dfFD[self.dfFD.columns[1]].tolist()
            for i in range(0, len(col1)):
                #print(str('t1&t2&EQ(t1.' +  col1[i] + ',t2.' + col1[i] + ')&IQ(t1.' + col2[i] + ',t2.' + col2[i] + ')' + '\n'))
                fname.write('t1&t2&EQ(t1.' +  col1[i] + ',t2.' + col1[i] + ')&IQ(t1.' + col2[i] + ',t2.' + col2[i] + ')' + '\n')
            os.remove("output.csv")
        else:
            print("Please load the pre-manipulated denialConstraints file manually \n")
            
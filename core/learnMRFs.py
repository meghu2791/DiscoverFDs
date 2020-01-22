from core.abstract import BaseDB
import numpy as np

class learnMRF(BaseDB):

    def __init__(self, data):
        super(learnMRF, self).__init__(data)

    def createMRFs(self):
        self.preprocessing()
        self.groupattributes()
        self.MRFs_probability = []
        col_names = self.df.columns
        #print col_names
        for j in range(0, len(self.list_probabilityOfAB)):
            #print self.list_probabilityOfAB[j]
            for i in range(0, len(self.list_probabilityOfAB[j])):
                if j!=i:
                    temp = np.exp(-self.list_probabilityOfAB[j][i])
                    self.MRFs_probability.append(temp)
                    if temp < 0.4:
                        #print(col_names[j], '-', col_names[i], '-', temp)
                        self.file_FD.write(col_names[j] + ',' + col_names[i] + ',' + str(temp) + '\n')
        #print len(self.list_probabilityOfAB[2])
        

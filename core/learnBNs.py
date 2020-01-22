from abstract import Profiler
import numpy as np

class learnBN(Profiler):

    def __init__(self):
        super().__init__()

    def createBNs(self):
        rand_smpl = []

        count = 0
        self.BNs_probability = []
        self.BNs_A = []
        self.sampling_A = []
        self.list_findDependency_bayes_AB = []
        self.list_findDependency_bayes_BA = []


        self.preprocessing()
        self.groupattributes()
        self.probability_columns()

        #Computing P(A and B), P(A), P(B)
        for j in range(len(self.list_probabilityOfAB)):
            sample_interval = int(len(self.list_probabilityOfAB[j]) / 10)
            for i in range(0, len(self.list_probabilityOfAB[j]), sample_interval + 1):
                iter_int = int(np.random.randint(0, len(self.list_probabilityOfAB[j])))
                rand_smpl.append(self.list_probabilityOfAB[j][iter_int])
                count = count + 1
            self.BNs_probability.append(sum(rand_smpl)/count)
        count = 0

        for j in range(len(self.list_probability)):
            sample_interval = int(len(self.list_probability[j]) / 10)
            for i in range(0, len(self.list_probability[j]), sample_interval + 1):
                iter_intA = int(np.random.randint(0, len(self.list_probability[j])))
                self.sampling_A.append(self.list_probability[j][iter_intA])
                count = count + 1
            self.BNs_A.append(sum(self.sampling_A)/count)
        count = 0

        ### build Bayesian network
        ##Calculate P(B/A)=P(A and B)/P(B)
        length = (self.list_probabilityOfAB.__len__())

        for i in range(length):
        # print(list_probabilityOfAB.__getitem__(i))
            val = self.BNs_probability.__getitem__(i % length) /  self.BNs_A[(i + 1) % length]
            self.list_findDependency_bayes_AB.append(val * self.BNs_A[i % length] / self.BNs_A[(i + 1) % length])
        #print(self.list_findDependency_bayes_AB)

            ###TODO print dependencies -> 2 sided high probabilities, they aren't directional -> they will hold pairwise markow props

        for i in range(length):
            # print(list_probabilityOfAB.__getitem__(i))
            val = self.BNs_probability.__getitem__((i + 1) % length) / self.BNs_A[i % length]
            self.list_findDependency_bayes_BA.append(val * self.BNs_A[(i + 1) % length] / self.BNs_A[i % length])
        #print(self.list_findDependency_bayes_BA)

        parent = []
        child = []
        
        for i in range(length):
            if (np.abs(self.list_findDependency_bayes_AB[i] - self.list_findDependency_bayes_BA[i]) < 0.2):
                continue
            else:
                if ((self.list_findDependency_bayes_AB[i]) > 0.9):
                    print(self.df.columns[i + 1] + "->" + self.df.columns[i])
                    parent.append(self.df.columns[i + 1])
                    child.append(self.df.columns[i])
                if ((self.list_findDependency_bayes_BA[i]) > 0.9):
                    print(self.df.columns[i] + "->" + self.df.columns[i + 1])
                    parent.append(self.df.columns[i])
                    child.append(self.df.columns[i + 1])

        for idx, i in enumerate(child):
            self.file_FD.write(parent[idx] + '->' + child[idx] + '\n')

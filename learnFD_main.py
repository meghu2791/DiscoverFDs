from core.learnMRFs import learnMRF
from core.learnBNs import learnBN
import sys

def main():
    #fname = open("flight_1k.csv", 'r+')
    mrf = learnMRF(sys.argv[1])
    mrf.createMRFs()
    mrf.factorGraphs()

    bn = learnBN(sys.argv[1])
    bn.createBNs()

if __name__ == '__main__':
    main()
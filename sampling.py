#http://opendata.stackexchange.com/questions/1256/how-can-i-work-with-a-4gb-csv-file
#Model Assisted Survey Sampling - Sarndall. Chapters 2 and 3

"""
SAMPLING ALGORITHMS
The algorithms implemented allow to select elements in a single sequential run over the database.
"""

import random

filepath = "C:/Users/user/Documents/MD/Bimbo dataset/"
in_file = filepath + "train.csv"
N = 74180465 #population size
n = 1000000 #desired sample size


def bernoulliSampling():
    """Bernoulli Sampling.
        List sequential algorithm.
    """
    out_file = filepath + "bernoulli_sample.csv"
    pi = n/float(N) #0.013480638062864665
    with open(in_file, 'r') as inf, open(out_file, 'w') as outf:
        header = inf.readline() #reads the header
        outf.write(header)
        for line in inf:
            newrandom = random.SystemRandom().random()
            if newrandom < pi:
                outf.write(line)

def simpleRandomSampling():
    """Simple Random Sampling (without replacement).
        List sequential algorithm: FAN-MULLER.
    """
    out_file = filepath + "simple_random_sample.csv"
    with open(in_file, 'r') as inf, open(out_file, 'w') as outf:
        nk = 0 #selected elems
        k = 0 #elem index
        header = inf.readline() #reads the header
        outf.write(header)
        for line in inf:
            k = k + 1
            p = (n - nk)/ float(N - k + 1) #probability of elem k
            newrandom = random.SystemRandom().random()
            if newrandom < p:
                nk = nk + 1
                outf.write(line)

def systematicSampling():
    """Systematic Sampling.
        List sequential algorithm.
    """
    out_file = filepath + "systematic_sample.csv"
    with open(in_file, 'r') as inf, open(out_file, 'w') as outf:
        a = int(N/float(n)) #jump range
        r = random.SystemRandom().randint(1,a) #init position
        k = 0 #elem index
        header = inf.readline() #reads the header
        outf.write(header)
        for line in inf:
            k = k + 1
            if (k - r) % a == 0:
                outf.write(line)

#total demand: 535921510.0
#Bernoulli variance: 2.71054561139e+12
#Simple Random variance: 2.59020903454e+12
#Systematic variance: 2.54269659073e+12

def calculateTotal(): 
    out_file = filepath + "total.txt"
    total = 0
    with open(in_file, 'r') as inf, open(out_file, 'w') as outf:
        header = inf.readline() #reads the header
        for line in inf:
            demanda = line.split(',')[-1]
            total = total + float(demanda)
        print total
        outf.write(str(total))

def sampleSize():
    """Computes the adecuate sample size when estimating the SUM of the population data
        Population sum is 535.921.510
    """
    import pylab as pl
    import numpy as np
    import math
    
    Z = 1.96 #Confidence level of 95%
    Syu2 = 477.1442158 #Population variance, estimated with a pilot sample.
    N = 74180465 #Population size
    n0 = (Z**2)*(N**2)*(Syu2)

    def n(EM):
        return n0 / (EM**2 + n0/N)

    EM = np.arange(0.0, 10000000.0, 100.0) #Margins or errors to evaluate
 
    pl.figure()
    pl.plot(EM, n(EM))
    pl.xlabel("Margin of error")
    pl.ylabel("Sample size")
    pl.show()

    #with n = 1000000, EM is 3154447.19033
    nf = 1000000
    print math.sqrt( (n0/float(nf)) - (n0/float(N)) )

def sampleSize2():
    """Computes the adecuate sample size when estimating the AVERAGE of the population data.
        Population average is 7,25
    """
    import pylab as pl
    import numpy as np
    import math
    
    Z = 1.96 #Confidence level of 95%
    Syu2 = 477.1442158 #Population variance, estimated with a pilot sample.
    N = 74180465 #Population size
    n0 = (Z**2)*(Syu2)

    def n(EM):
        return n0 / (EM**2 + n0/N)

    EM = np.arange(0.0, 0.1, 0.0001) #Margins or errors to evaluate

    pl.figure()
    pl.plot(EM, n(EM))
    pl.xlabel("Margin of error")
    pl.ylabel("Sample size")
    pl.show()

    #with n = 1000000, EM is 0.0425239608613
    nf = 1000000
    print math.sqrt( (n0/float(nf)) - (n0/float(N)) )

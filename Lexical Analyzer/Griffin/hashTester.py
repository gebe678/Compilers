#!/usr/bin/python3
#   
#   Noah Olmstead Harvey
#   
#   2021.10.20
#   
#   script for testing the distribution of english words with various hashing methods

####  IMPORTS  #################################################################################################################

from lexilyzer import hasher                                    #   for hash testing
from lexilyzer import openFile                                  #   for hash testing
from matplotlib import pyplot as plt                            #   for hash testing
import seaborn as sns                                           #   for hash testing

####  GLOBALS  #################################################################################################################

####  FUNCTIONS  ###############################################################################################################

####  MAIN  ####################################################################################################################

def main():
    engDict = openFile("engDict.txt").split()

    numberHash,indexHash,fPrimeHash,lPrimeHash,pPrimeHash = [],[],[],[],[]

    for word in engDict:
        numberHash.append(hasher(word,"number"))
        indexHash.append(hasher(word,"index"))
        fPrimeHash.append(hasher(word,"fPrime"))
        lPrimeHash.append(hasher(word,"lPrime"))
        pPrimeHash.append(hasher(word,"pPrime"))

    plt.figure(figsize=(12,12))
    plt.subplot(321)
    sns.distplot(numberHash,color='b',label="number",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.subplot(322)
    sns.distplot(indexHash,color='b',label="index",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.subplot(323)
    sns.distplot(fPrimeHash,color='b',label="first primes",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.subplot(324)
    sns.distplot(lPrimeHash,color='b',label="large primes",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.subplot(325)
    sns.distplot(pPrimeHash,color='b',label="prime primes",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.subplot(326)
    sns.distplot(numberHash,color='r',label="number",bins=499,kde_kws={"shade":True,"bw_method":.01})
    sns.distplot(fPrimeHash,color='g',label="first primes",bins=499,kde_kws={"shade":True,"bw_method":.01})
    sns.distplot(pPrimeHash,color='b',label="prime primes",bins=499,kde_kws={"shade":True,"bw_method":.01})
    plt.xlim(-1,500)
    plt.ylim(0,.003)
    plt.legend()
    plt.savefig("hashComparison.pdf")

if(__name__=="__main__"): main()                                #   runs main if script launched from command line
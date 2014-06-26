#!/usr/bin/env python
#PROGRAM: PLT

#This program will output a plot of the input data structure.
import sys
import os
import numpy as np
import math
import matplotlib.pyplot as plt
def pltbare(data,xaxis,yaxis):
    f = plt.figure()
    p1,=plt.plot(data[0],data[1])
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.xscale('log')
    plt.yscale('log')
    return f
    
def pltfreqnoise(data,xaxis,yaxis,VP,FWHM):
    f = plt.figure()
    p1,=plt.plot(data[0],data[1]*FWHM/VP)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.xscale('log')
    plt.yscale('log')
    return f

if __name__ == '__main__':
    dataName = sys.argv[1]
    xax = sys.argv[2]
    yax = sys.argv[3]
    outName = dataName.split('.')[0]+'plt'

    data = np.loadtxt(dataName, unpack=True)
    bareplot = pltbare(data,xax,yax)
    bareplot.savefig(outName+'.eps')
    plt.close(bareplot)

    #freqplot = pltfreqnoise(data,xax,r'$\mathrm{Hz/\sqrt{Hz}}$',.3,15*10**6)
    #freqplot.savefig(outName+'freq.eps')
    #plt.close(freqplot)

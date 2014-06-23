#!/usr/bin/env python
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import sys
import argparse
#COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description='Creating output data from the machzender delay line frequency data setup')
parser.add_argument('filename',help="The filename of the raw data")
parser.add_argument('noisenoise',help='The filename of the noise data')
parser.add_argument("delV",help='The change in voltage recorded by the voltmeter',type=float)
parser.add_argument("delay",help="The length of the delay line",type=float)
parser.add_argument("out", help="The output file name",default="out")
args=parser.parse_args()
data = np.loadtxt(args.filename,unpack=True)
datanoise=np.loadtxt(args.noisenoise, unpack=True)
fnumber= args.delay*1.45846/(3.*10**8) #index of fused silca
#fnumber is the delay time

#now, preform the operations on the data
def totalPower(power, noiseflr):
    out = np.sqrt(power**2.-noiseflr**2.)
    return out

def totalPower2(power, noiseflr):
    #For when the data is taken in V^2/Hz
    out = power/2. -noiseflr/2
    return out

def total_freq(freq,power,delV,delay):
    aveV=(delV)
    out=power/(((aveV/2.)**2.)*2.*((np.sin(np.pi*freq*(delay)))**2.)/(freq**2.))
    return out
#outdata =np.vstack((data[0], total_freq(data[0],data[1]/2.-datanoise[1]/2. ,args.delV,fnumber))).T

outdata =np.vstack((data[0], total_freq(data[0],data[1]**2. ,args.delV,fnumber))).T
np.savetxt('%smacout.dat' %args.out, outdata)
print "%s"%args.out

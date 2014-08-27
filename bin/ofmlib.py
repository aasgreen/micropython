#!/usr/bin/env python
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import sys
import argparse




#Python Library for OFM use

class Mach:
    def __init__(self, dataname, vmax, vmin, delay, outname):
        self.name = dataname
        self.out = outname
        self.aveV = vmax-vmin
        self.delay =delay*1.45846/(3.*10**8) #index of fused silca
        self.data = np.loadtxt(dataname,unpack=True)
        self.freq = self.data[0]
        self.fnoise = self.freqnoise()
        self.save(self.freq,self.fnoise,self.out)

    def save(self,freq,noisepower,outname):
        np.savetxt(outname,np.vstack([freq,noisepower]).T)

    def sens(self, data):
        power = data[1]**2.
        freq = data[0]
        return power/(((self.aveV/2.)**2.)*2.*((np.sin(np.pi*freq*(self.delay)))**2.)/(freq**2.))
        
    def freqnoiseFloor(self,noisefloordata):
        self.noisefloor = np.loadtxt(noisefloordata,unpack=True)
        return self.sens(self.noisefloor)

    def freqnoise(self):
        return np.vstack([self.data[0],self.sens(self.data)])

class Allan:
    def __init__(self, dataname, gatetime):
        self.name = dataname
        self.data = np.genfromtxt(dataname, unpack=True)
        self.gate = gatetime
        self.carrier = 3.*10**(8)/(1550. *10**(-9))
        self.m = np.unique(np.trunc(np.logspace(0,np.log10(self.data.size // 10. ),num=100)))
        #create an array for m that stops when the data can be divided into 5 sections.
        self.time = np.array([i*self.gate*10**(-3) for i in range(self.data.size)])
        self.tau = self.m*self.gate*10**-3
        self.normdat,self.thermfit = self.ftofracfreq()
        self.outvar = np.fromiter((np.sqrt(self.var(self.normdat,int(n))) for n in self.m),dtype=float)

    def ftofracfreq(self):
        p = np.polyfit(self.time, self.data,1)
        data_nodrift = self.data-np.polyval(p,self.time)
        dcarrier = np.mean(data_nodrift)
        data_frac = (data_nodrift-dcarrier)/self.carrier
        return data_frac, p
    def x(self, y):
        return y

    def var(self,freq,m):
    #Compute the allan_variance of data with gatetime/spacing of dt
        mean2 = freq[:(freq.size // m ) * m].reshape(-1,m).mean(axis=1)
        print mean2.size
        print m
        alvar = 1/2./(mean2.size-1) * np.sum(np.fromiter(((mean2[i+1]-mean2[i])**2 for i in range(0,mean2.size-1)),dtype=float))
        return alvar




#COMMAND LINE ARGUMENTSf 
if __name__ =="__main__":
             
    parser = argparse.ArgumentParser(description='Creating output data from the machzender delay line frequency data setup')
    parser.add_argument('filename',help="The filename of the raw data")
    #parser.add_argument('noisenoise',help='The filename of the noise data')
    parser.add_argument("MaxV",help='The max voltage recorded by the voltmeter',type=float)
    parser.add_argument("MinV",help='The min voltage recorded by the voltmeter',type=float)
    parser.add_argument("delay",help="The length of the delay line",type=float)
    parser.add_argument("out", help="The output file name",default="out")
    args=parser.parse_args()
    mzen = Mach(args.filename, args.MaxV, args.MinV, args.delay, args.out)
    #data = np.loadtxt(args.filename,unpack=True)
    #datanoise=np.loadtxt(args.noisenoise, unpack=True)
    #fnumber= args.delay*1.45846/(3.*10**8) #index of fused silca
    #fnumber is the delay time
    #outdata =np.vstack((data[0], total_freq(data[0],data[1]**2. ,args.MaxV,args.MinV,fnumber))).T
    np.savetxt('%smacout.dat' %args.out, np.vstack([ mzen.fnoise]).T)
    #print "%s"%args.out

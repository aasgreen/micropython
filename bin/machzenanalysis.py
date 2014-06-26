#!/usr/bin/env python
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
lockedPDHnoise = np.loadtxt("01282014-1519-s1.dat",unpack=True)
noisefloor = np.loadtxt("-10dBm_noise_floor.txt",unpack=True)
noisefloor6 = np.loadtxt("-6dBm_noise_floor.txt",unpack=True)
lockedCavitynoise = np.loadtxt("01282014-1534-s3.dat",unpack=True)
freeRunning = np.loadtxt("01282014-1534-s2.dat", unpack=True)

#now, preform the operations on the data
def totalPower(power, noiseflr):
    out = np.sqrt(power**2.-noiseflr**2.)
    return out

def total_freq(freq,power,noiseflr,maxV,minV):
    totalPow = power**2.-noiseflr**2.
    aveV=(maxV-minV)/2.
    out=totalPow/(((aveV/2.)**2.)*2.*((np.sin(np.pi*freq*(9.55881254169446*10**-7.)))**2.)/(freq**2.))
    return out
totalFreqPDH = total_freq(noisefloor6[0],lockedPDHnoise[1],noisefloor[1],.8901,.2655)
totalFreqLoop = total_freq(noisefloor6[0],lockedCavitynoise[1],noisefloor6[1],.6945,.1880)
freeRunnoise=total_freq(noisefloor6[0],freeRunning[1],noisefloor6[1],.8996,.2514)
#plt.figure()
#p1,=plt.plot(freeRunning[0],totalFreqPDH)
#p2,=plt.plot(freeRunning[0],totalFreqLoop)
#p3,=plt.plot(freeRunning[0],freeRunnoise)
#plt.xscale('log')
#plt.yscale('log')
#plt.legend([p1,p2,p3],['PDH Lock','Side Cavity Lock','FreeRun'])
#plt.ylim([10**2,10**8])
#plt.xlabel('Hz')
#plt.ylabel(r'$\frac{\mathrm{Hz}}{\sqrt{\mathrm{Hz}}}$')
#plt.savefig('machzenlock.eps')
#plt.show()
#np.savetxt("totalFreqPDH.dat", totalFreqPDH)
#np.savetxt("totalFreqLoop.dat",totalFreqLoop)
#np.savetxt("freeRunnoise.dat",freeRunnoise)

#Now, I also want to calculate the allan variance
from scipy import integrate
def allan(freq,noise, t):
    #first, convert to phase noise
    phase=np.float_(noise*1.934*(10**14)/2./(freq**2.))
    #now integrate over all values to get allan variance
    transferFunc = np.float_(np.sin(np.pi*phase*t)**4/(np.pi*t*phase)**2)
    out = 2*integrate.trapz(phase*transferFunc,freq)
    return np.sqrt(out)

#Now, calculate the allan deviation for all three
t = np.linspace(0,1,6000)
allPDH = [allan(freeRunning[0],totalFreqPDH,tau) for tau in t]
allLoop= [allan(freeRunning[0],totalFreqLoop,tau) for tau in t]
allFree= [allan(freeRunning[0],freeRunnoise,tau) for tau in t]
plt.figure(2)
plt.figure()
p4,=plt.loglog(t,allPDH)
p5,=plt.plot(t,allLoop)
p6,=plt.plot(t,allFree)
plt.legend([p4,p5,p6],['PDH Lock','Side Cavity Lock','FreeRun'])
plt.xlabel(r'$\tau$')
plt.ylabel(r'Allan Variance')
#plt.savefig('machzenlock.eps')
#
plt.show()

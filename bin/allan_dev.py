#!/usr/bin/env python

#Code created by adam green while at NIST. Frusterated by other code that I tried to get to work, or
#found too complex for what should be a simple job. This is part of a larger effort by me to create
#a working library for the time and frequency needs.

import numpy as np
from matplotlib import pyplot as plt
import sys, argparse
from scipy import integrate

def allan_var(data, dt,m):
#Compute the allan_variance of data with gatetime/spacing of dt
    #mean2 = np.fromiter((np.mean(data[i:i+m]) for i in range(0,data.size, m)),dtype=float)
    #mean2 = np.array([np.mean(t) for t in mean1])
    mean2 = data[:(data.size // m ) * m].reshape(-1,m).mean(axis=1)
    #print mean2
    print mean2.size
    print m
    alvar = 1/2./(mean2.size-1) * np.sum(np.fromiter(((mean2[i+1]-mean2[i])**2 for i in range(0,mean2.size-1)),dtype=float))
    return alvar

def modalvar(data,dt,m):
 #Compute the modified allan_variance of data with gatetime/spacing of dt
    mean1 = np.array([data[i:i+m] for i in range(0,data.size)])
    mean2 = np.array([np.mean(t) for t in mean1])
    alvar = 1/2./(mean2.size-1) * np.sum(np.array([(mean2[i+1]-mean2[i])**2 for i in range(0,mean2.size-1)]))
    return alvar 

def modalvar2(data,dt,m):
    dt = dt*10.**(-3)
    #first integrate to get phase noise
    x = integrate.cumtrapz(data, x=None, dx = dt*10.**(-3))
    alvar = 0
    for i in range(0,x.size-2*m):
        alvar += 1/2./((x.size-2.*m)*dt**2.)*(x[i+2*m]-2.*x[i+m]+x[i])**2.
    return alvar
#First, we need to convert the absolute frequency time series into fraction frequency deviations.
def ftofracfreq(freq,time, carrier):
    p = np.polyfit(time, freq,1)
    data_nodrift = data-np.polyval(p,time)
    dcarrier = np.mean(data_nodrift)
    data_frac = (data_nodrift-dcarrier)/carrier
    return data_frac, p


#First, we need to remove the frequency drift, and convert our data into fractional frequency flucuations.

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="This script will calculate the allan variance from a time series data", version='1')
    parser.add_argument("dataName", help="The filename of the raw time series data")
    parser.add_argument("gate", help="The gate time of the frequency counter, in ms")
    args=parser.parse_args()
    dt = float(args.gate)
    args= parser.parse_args()
    print args.dataName
    dataName = str(args.dataName)
    data = np.loadtxt(dataName, unpack=True)
    time = [dt*i*10**(-3) for i in range(data.size)]

    #Now that data is loaded, remove frequency drift
    carrier = 3.*10**(8)/(1550. *10**(-9))
    f,p = ftofracfreq(data, time, carrier)

    if (data.size*dt*10**-3 >30.):
        m = np.unique(np.trunc(np.logspace(0,np.log(30.//(dt*10**-3) )/np.log(10.),num=100)))
        print 'only ten'
    else:
        m = np.unique(np.trunc(np.logspace(1,np.log(data.size // 2.1 )/np.log(10),num=100)))
    #m = np.linspace(1,10./(dt*10**(-3)))
    print m
    al = [np.sqrt(allan_var(f, dt, int(n))) for n in m]
    al2 = [np.sqrt(allan_var(data/carrier, dt, int(n))) for n in m]
    plt.subplot(3,1,1)
    plt.loglog(m*dt*10**-3, al,'.')
    plt.loglog(m*dt*10**-3, al2,'.')
    plt.subplot(3,1,2)
    plt.plot(time, data)
    plt.plot(time, np.polyval(p,time))
    plt.subplot(3,1,3)
    plt.plot(time,f)
    plt.show() 
    print "total Time of measurement = "+ str(data.size*dt*10**(-3))
    print "Fitting values:"+str(p)
    #Now save the text files of the allan deviation for future reference

    outName = dataName.split('.')[0]+'.plt'
    np.savetxt(outName, np.c_[m*dt*10**-3, al2],footer="Generated by allan_dev, written by A. G.",comments="#")

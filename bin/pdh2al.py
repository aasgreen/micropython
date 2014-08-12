import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import sys
import argparse
from scipy.integrate import trapz
#FUNCTIONS DEFINED########
def al(tau, noise_psd, freq):
    kern = lambda t:[ s*np.sin(np.pi*f*t)**4/(np.pi*carrier*t)**2 for s,f in zip(noise_psd,freq)]
    kernFreq = lambda t:[ s*np.sin(np.pi*f*t)**4./(np.pi*f*t)**2. for s,f in zip(noise_psd,freq)]
    out = 2. *trapz(kernFreq(tau),freq)#*10.**-24
    return out

def alexpand(tau, noise_psd, freq, one2tennoise):
    kern = lambda t:[ s*np.sin(np.pi*f*t)**4/(np.pi*carrier*t)**2 for s,f in zip(noise_psd,freq)]
    kernFreq = lambda t:[ s*np.sin(np.pi*f*t)**4./(np.pi*f*t)**2. for s,f in zip(noise_psd,freq)]
    fone2ten = np.logspace(-9,1,num=50)
    alfromone2ten = 2*trapz([one2tennoise*100+.01*one2tennoise/f+.1*one2tennoise/f**2.*np.sin(np.pi*f*tau)**4./(np.pi*f*tau)**2 for f in fone2ten],fone2ten)
    out = 2. *trapz(kernFreq(tau),freq)+alfromone2ten
    #out = alfromone2ten
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creating output data from the machzender delay line frequency data setup')
    parser.add_argument('filename',help="The filename of the raw data")
    parser.add_argument('type',help='Type of data (x,y): phase or freq')
    args=parser.parse_args()
    data = np.loadtxt(args.filename,unpack=True)

    
    noise_psd = data[0]
    freq = data[1]



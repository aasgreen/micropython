import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
import sys
import argparse
from scipy.integrate import simps
#FUNCTIONS DEFINED########
def al(tau, noise_psd, freq):
    kern = lambda t:[ s*np.sin(np.pi*f*t)/(np.pi*carrier*tau)**2 for x,y in zip(noise_psd,freq)]
    ker_freq= lambda t:[ s*np.sin(np.pi*f*t)/(np.pi*f*tau)**2 for x,y in zip(noise_psd,freq)]
    if args.type == 'phase':
        out =  2*integrate.simps(kern(tau),freq)
    elif args.type =='freq':
        out = 2 *integrate.simps(kern_freq(tau),freq)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creating output data from the machzender delay line frequency data setup')
    parser.add_argument('filename',help="The filename of the raw data")
    parser.add_argument('type',help='Type of data (x,y): phase or freq')
    args=parser.parse_args()
    data = np.loadtxt(args.filename,unpack=True)

    
    noise_psd = data[0]
    freq = data[1]



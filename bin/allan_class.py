# Calculation of Allan Variance
# For Senior Design: Complex programmable logic device for analysis and synchronization of oscillators
# Scott Schafer
#
# use in bash to include scipy in path:
#   PYTHONPATH=$HOME/local/lib/python2.6/site-packages python
# OR in python:
# import sys
# sys.path.append("/home/sschafer/local/lib/python2.6/site-packages")
import time, sys, time, csv, types, math
#sys.path.append("/home/sschafer/local/lib/python2.6/site-packages")
import numpy, scipy


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid import AxesGrid

DEBUG = True


##################################################
# Class Functions
    # General
        # __init__ : initialization function
        # load : loads data file specified
        # set_section : sets the splice value for analysis and plotting
        # first_diff : initialization function to calculate various arrays used for the allan variance
    # Analysis
        # allan_single : finds the allan variance for a single m value
        # allan_multi : finds the allan variance for all m values
    # Plotting
        # plot_data : plots cumulation of counts (raw data)
        # plot_fd : plots first difference of data (counts per second)
        # plot_linfit : plots linear regression of the cumulation of points
        # plot_single : plots allan variance for a single m value (just second difference?)
        # plot_multi : plots sigma squared for all m values (sigma sq vs m)
# Global Variables
#   filename = File of data on disk.  Used for all analysis until a different file is loaded
#   section = Slice of data to use from file.  Used unless a different slice is specified when using analysis function. 
#       0: start point, 1: end point
#       there are no local slices! - specifying slice using analysis function will change the global slice value
#   leng = length of data set
#
# Data Variables:
#   data = raw count data from file
#   t = 'time' variable (based on assumed data point per second),  time from datafile is NOT used (it is the time that the computer recieves the info)
#   fd = first difference of data
#   
#   x = fractional frequency of data
#   xx = fractional frequency of linear regression of data
#   
#   sd = second difference of fractional frequency (xx)
#   [m, sq] = sigma_sq[i] = allan variance (sq or sigma squared) for m value

class Allan:
    #initialization function
    def __init__(self, datafile, sec=None):
        self.filename = datafile
        self.first_diff()
        self.set_section(sec)
        self._single = False # private variable flag if corresponding analysis has been done (allows plotting)
        self._multi = False
        if (DEBUG):
            print "Done with initialization"
    
    #load or reload datafile
    def load(self, datafile, sec=None):
        self.filename = datafile
        self.first_diff()
        self.set_section(sec)
        self._single = False
        self._multi = False
        if (DEBUG):
            print "Done loading file"
    
    # parse the input for the slice value
    def set_section(self, sec):
        try:
            if sec is None: # previous slice values
                return
            elif (sec == 'All' or sec == 'a' or sec == 'A'): # use entire data set
                self.section = [0, self.leng]
            elif (type(sec) == types.ListType or type(sec) == types.TupleType):
                if (len(sec) == 1): # specify start of slice
                    self.section = [sec[0], self.leng]
                elif (len(sec) == 2 and sec[1] > sec[0]): # specify start and end of slice
                    self.section = [sec[0], sec[1]]
                else:
                    print "ERROR: Invalid splice value.  Form: [start, end] or [start]"
                    print "\tUsing all data points"
            elif (type(sec) == types.IntType): # specify start of slice
                self.section = [sec, self.leng]
        except:
            print "ERROR: Invalid splice value.  Form: [start, end] or [start]"
            print "\tUsing all data points"
        
        # calculate the a linear regression of the cumulation of counts
        #   required for calculation of allan variance
        if (DEBUG):
            print "Finding Linear Regresion for data"
        [sp, ep] = [self.section[0], self.section[1]]
        p = numpy.polyfit(self.t[sp:ep], self.x[sp:ep], 1)
        if (DEBUG):
            print "Calculating xx"
        self.xx = self.x[sp:ep] - numpy.polyval(p,self.t[sp:ep])
        self._single = False
        self._multi = False
        return
    
    
    ##################################################
    #allan_multi
    #
    # finds the allan variance for all m values
    # Input:
    #   sec - slice of file data to use for plotting
    #   points - optional parameter to specify the number of m values to calculate at
    # Result:
    #   sigma_sq array of sigmas for m values
    #   
    def allan_multi(self, points=100, sec=None):
        self.set_section(sec)
        [sp, ep] = [self.section[0], self.section[1]]
        
        #to create log-log plot:
        #   calculate allan variance of entire data set with m*tau0 value (with sum!)
        #   plot m*tau0 versus allan variance, sigma^2(m*tau0)
        #step = scipy.linspace(0, leng/2.-1., points) # linear spaced values
        step = scipy.logspace(0, math.log10(len(self.xx)/4.-1.), points) # logarithmic spaced values
        m = numpy.floor(step)
        step = list(set(m))
        step.sort()
        
        N = numpy.zeros(len(step))
        self.sigma_sq = numpy.zeros((len(step),2))
        
        start = time.time()
        now = time.gmtime().tm_sec - 1
        index = 0
        for mtau in step:
            prev = now
            now = time.gmtime().tm_sec
            if (prev != now):
                print "i:", index, "mtau:", mtau, "to", len(self.xx)/4
            
            self.sigma_sq[index] = [mtau, self.allan_single(m=mtau)]
            index = index + 1
        
        self._multi = True
        self._single = False
        return
    
    
    ##################################################
    #allan_single
    #
    # finds the allan variance for a single m value
    # Input:
    #   section - slice of file data to use for plotting
    # Result:
    #   sd of data range (as given by section) for allan variance with m
    # Return:
    #   sigma of sd set for that m value
    #   
    def allan_single(self, m=1, sec=None):
        if (m < 1 or (m != math.floor(m))):
            print 'ERROR: Invalid m value: m must be an interger equal to or larger than 1'
            return
        self.set_section(sec)
        [sp, ep] = [self.section[0], self.section[1]]
        
        j = range(0, int(len(self.xx)-2*m), 1)
        if (len(j)== 0):
            print "short"
        N = len(j)
        self.sd = numpy.zeros(len(self.xx)-2*m)
        for i in j:
            self.sd[i] = (self.xx[i+2*m] + self.xx[i] - 2*self.xx[i+m])**2/(10e6**2)
        
        #if (DEBUG):
        #    print "N:", N, "m:", m
        sigma = math.sqrt( 1/(2*(N-2*m)*(m**2)) * sum(self.sd))
        self._single = True
        return sigma
    
    
    ##################################################
    #first_diff
    #
    # Function to find the first difference of a data set.  
    #   Assumes 2 column data (time, data)
    #
    # Input:
    #   none
    # Result:
    #   fd = first difference data set
    #       first difference is calculated starting on the second data point:
    #           fd(i) = data(i) - data(i-1)
    #       fd(0) is the same number as the first data point (no difference calculated)
    #   data = raw data stream
    #   t = time
    #   
    def first_diff(self):
        if (DEBUG):
            print "Importing data"
        fin = open(self.filename,'r')
        fin.readline()
        
        tmp = csv.reader(fin, delimiter=' ')
        raw = []
        for i in tmp:
            raw.append(i)
        
        if (DEBUG):
            print "Allocating arrays"
        leng = len(raw)
        width = len(raw[1])
        self.data = numpy.zeros(leng)
        self.t = numpy.zeros(leng)
        self.fd = numpy.zeros(leng)
        for i in range(0,leng):
            self.data[i] = raw[i][width-1]
            self.t[i] = raw[i][0]
        
        self.leng = len(self.t)
        self.fd[0] = self.data[0] # skip first data point (no history before first point)
        
        if (DEBUG):
            print "Finding first difference"
        for i in range(1,self.leng):
            self.fd[i] = self.data[i] - self.data[i-1]
        
        if (DEBUG):
            print "Calculating x"
        # x = (f1 - f0)/f0 * 1sec
        #   f0 = nominal frequency
        #   f1 = test oscillator frequency
        self.x = (self.data[:] - self.data[0])
        return
    
    
    ##################################################
    #unwrap
    #
    # Function to unwrap the data.  Finds the jumps when the data moves
    #   from 0 -> 10e7 (or vice versa) and moves data so there is no more
    #   large discontinuity.
    #
    # Input:
    #   filename output
    # Result:
    #   unwrapped data set is put in given filename
    #   
    def unwrap(self, filename="", export=False, fixjumps=True):
        if (DEBUG):
            print "Unwrapping data"
        
        if (export and filename == ""):
            print "Specify filename"
            print "Usage: Allan.unwrap(filname, export=True)"
            return
        
        wrap_percent = 0.9
        wrap_num = 0
        wrap_range = 10000000
        jump_value = 0
        pplot = False
        
        leng = len(self.data)
        self.wrap = numpy.zeros(leng)
        self.wrap[:] = self.data[:]
        for i in range(1,leng):
            if (numpy.abs(self.data[i] - self.data[i-1]) > wrap_range*(1-wrap_percent)):
                print "t:" + str(self.t[i-1]) + " : " +str(self.data[i-1]) + "->" + str(self.data[i]) + "   percent: " + str((self.data[i] - self.data[i-1])/wrap_range)
                if ((self.data[i] - self.data[i-1]) > wrap_range*wrap_percent):
                    wrap_num = wrap_num - 1
                    print str(self.data[i-1]) + "->" + str(self.data[i]) + "   wrap_num: " + str(wrap_num)
                elif ((self.data[i-1] - self.data[i]) > wrap_range*wrap_percent):
                    wrap_num = wrap_num + 1
                    print str(self.data[i-1]) + "->" + str(self.data[i]) + "   wrap_num: " + str(wrap_num)
                else:
                    jump_value = jump_value + (self.data[i-1] - self.data[i])
                    print "\tjump: " + str(jump_value)
                pplot = True
            
            self.wrap[i] = self.data[i] + wrap_num * wrap_range
            if (fixjumps):
                self.wrap[i] = self.wrap[i] + jump_value
            
            if (pplot):
                plt.figure()
                plt.plot(self.t[:],self.wrap[:])
                plt.show()
                pplot = False
                
        
        if (export):
            fout = open(filename,'w')
            fout.write('Time    Count\n')
            for i in range(0,leng):
                fout.write(str(self.t[i]) + "  " + str(self.wrap[i]) + "\n")
            fout.close()
        else:
            self.data = self.wrap
            
        return
    
    
    
    
    ##################################################
    # plot_data : plots cumulation of counts (raw data)
    def plot_data(self):
        [sp, ep] = [self.section[0], self.section[1]]
        
        #plt.ioff()
        plt.figure()
        plt.plot(self.t[sp:ep],self.data[sp:ep])
        plt.title('Raw Data (' + self.filename + ')')
        plt.xlabel('Time (s)')
        plt.ylabel('Counts/Second')
        #plt.ion()
        
        plt.show()
        return
    
    # plot_fd : plots first difference of data (counts per second)
    def plot_fd(self):
        [sp, ep] = [self.section[0], self.section[1]]
        
        plt.figure()
        plt.plot(self.t[sp:ep],self.fd[sp:ep])
        plt.title('First Difference (' + self.filename + ')')
        plt.xlabel('Time (s)')
        plt.ylabel('Counts/Second')
        
        plt.show()
        return
    
    # plot_linfit : plots linear regression of the cumulation of points
    def plot_linfit(self):
        [sp, ep] = [self.section[0], self.section[1]]
        
        plt.figure()
        plt.plot(self.t[sp:ep],self.xx)
        plt.title('Regression of Raw Data (' + self.filename + ')')
        plt.xlabel('Time (s)')
        plt.ylabel('Counts/Second')
        
        plt.show()
        return
    
    # plot_single : plots allan variance for a single m value (just second difference?)
    def plot_single(self):
        if (self._single == True):
            [sp, ep] = [self.section[0], self.section[1]]
            
            plt.figure()
            plt.plot(self.sd)
            plt.title('Second Difference (' + self.filename + ')')
            plt.xlabel('Time (s)')
            plt.ylabel('')
            
            plt.show()
        else:
            print "Data has not been analyzed.  Run allan_single."
        return
    
    # plot_multi : plots sigma squared for all m values (sigma sq vs m)
    def plot_multi(self):
        if (self._multi == True):
            [sp, ep] = [self.section[0], self.section[1]]
            
            plt.figure()
            plt.loglog(self.sigma_sq[:,0],self.sigma_sq[:,1])
            plt.title('Allan Variance vs m (' + self.filename + ')')
            plt.xlabel('m')
            plt.ylabel('Sigma^2')
            
            plt.show()
        else:
            print "Data has not been analyzed.  Run allan_multi."
        return
    
    















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

class tex:
    '''This is going to have the structure that will give the tex file
    with the output being a description of each data, and the plot attatched to it
    '''
    def __init__(self,list_of_figs,description):
        self.fignames=list_of_figs
        self.des =description
        self.header = "\\documentclass{article}\n"
        self.packages =("\\usepackage{hyperref, graphics,float,graphicx,tabularx,pgfplots,pfdlscape,rotating}\n")
        self.title  =("\\begin{document}\n \\title{Datasheet for Folder} \n \\date{\\today} \n \\author{Adam Green} \n \\maketitle ")
        
    def create(self):
        with open('summary.tex','wb') as texfile:
            texfile.write(self.header);
            texfile.write(self.packages);
            texfile.write(self.title);
            texfile.write("\\end{document}")
        os.system("pdflatex summary.tex")
        os.system("open summary.pdf")


if __name__ == '__main__':
    dataName = sys.argv[1]
    xax = sys.argv[2]
    yax = sys.argv[3]
    outName = dataName.split('.')[0]+'plt'

    data = np.loadtxt(dataName, unpack=True)
    bareplot = pltbare(data,xax,yax)
    bareplot.savefig(outName+'.eps')
    plt.close(bareplot)

    freqplot = pltfreqnoise(data,xax,r'$\mathrm{Hz/\sqrt{Hz}}$',.3,15*10**6)
    freqplot.savefig(outName+'freq.eps')
    plt.close(freqplot)

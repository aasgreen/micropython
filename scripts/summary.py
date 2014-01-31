import sys
import os
class tex:
    '''This is going to have the structure that will give the tex file
    with the output being a description of each data, and the plot attatched to it
    '''
    def __init__(self,list_of_figs,description):
        self.fignames=list_of_figs
        self.des =description
        self.header = "\\documentclass{beamer}\n"
        self.packages =("\\usepackage{hyperref, graphics,float,graphicx,tabularx,pgfplots,adjustbox}\n")
        self.title  =("\\begin{document}\n  \\title{Datasheet for Folder} \n \\date{\\today} \n \\author{Adam Green} \n \\frame{\\titlepage} \n ")
        
    def create(self):
        with open('summary.tex','wb') as texfile:
            texfile.write(self.header);
            texfile.write(self.packages);
            texfile.write(self.title);
            texfile.write("\\begin{frame} \n \\frametitle{Description Of Data}\n")
            texfile.write(self.des+"\n \\end{frame}\n");
            texfile.write("\\begin{frame}{t,allowframebreaks} \\frametitle{Data Table} \n")
            texfile.write("\\adjustbox{max height=\\dimexpr\\textheight-5.5cm\\relax,max width=\\textwidth}{")
            texfile.write("\\begin{tabularx}{\linewidth}{|p{4cm}|X|}\\hline\n")
            texfile.write("Name & Description \\\\ \\hline \\hline \n")
            for key, value in self.fignames.iteritems():
                texfile.write(key+"&"+value+"\\\\ \hline\n")
            texfile.write("\\end{tabularx}}\n")
            texfile.write("\\end{frame}")
            for key,value in self.fignames.iteritems():
                print key
                print value
                texfile.write("\\begin{frame} \n\\begin{figure}[H]\n")
                texfile.write("\\includegraphics[width=\linewidth]{./plt/freq/"+key.split(".")[0]+"pltfreq.eps}\n")
                texfile.write("\\end{figure}\n")
                texfile.write(value+"\n")
                texfile.write("\\end{frame}\n")
            texfile.write("\\end{document}")
        os.system("pdflatex summary.tex")
        os.system("open summary.pdf")
    
if __name__ == "__main__":
    d={}
    with open('description.txt','r') as f:
        for line in f:
            print line
            (name,des)=line.split("&")
            d[name]=des.strip()
    with open("readme.txt","r") as f2:
        des = f2.read()
    mfile = tex(d,des)
    mfile.create()

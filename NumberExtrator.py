#!/usr/bin/env python
import itertools
import sys
import os
import errno
import glob
from optparse import OptionParser

#==========================
keywords =["HT 275 GeV", "HT 325 GeV", "HT 375 GeV","HT 475 GeV","HT 575 GeV", "HT 675 GeV", "HT 775 GeV", "HT 875 GeV"]
LatexTitleEntries = ["275","325","375","475","575","675","775","875"]
filetext = []
MuonMCtext = []
HadMCtext = []
numberholder = []
MuonMCnumberholder = []
HadMCnumberholder = []
File_List = []
MuonMC_List = []
HadMC_List = []
for l in range (0,len(keywords)):
  numberholder.append(int(0))
  MuonMCnumberholder.append(int(0))
  HadMCnumberholder.append(int(0))
#==========================
  
class Table_Maker(object):
  def __init__(self):
    self.tableoptions = a.options
    self.Table_Options()

  def Table_Options(self):  
    if self.tableoptions.Make_Latex is True:
      print "\nMaking Table\n"
      prediction = []
      for i in range(0,len(numberholder)):
	prediction.append(numberholder[i]*a.TranslationFactor[i])
      self.Latex_Table(numberholder,MuonMCnumberholder,HadMCnumberholder,a.TranslationFactor, 
                      rows = [{"label": r'''MC W + $\ttNew$''',         "entryFunc":HadMCnumberholder},
                            {"label": r'''MC $\mu +$~jets''',         "entryFunc":MuonMCnumberholder},
                            {"label": r'''MC Ratio''',                "entryFunc":a.TranslationFactor},
                            {"label": r'''Data $\mu +$~jets''',       "entryFunc":numberholder},
		            {"label": r'''W + $\ttNew$ Prediction''', "entryFunc":prediction},
                            ])

    if self.tableoptions.Make_Ted is True:
      print "\nMaking Teds Numbers"
   
  def toString(self,item) :
    if type(item) is int : return str(int(item))
    if type(item) is float : 
	item = "%5.2f"%item
	return str(float(item))
    else : return str(item)
 
  def oneRow(self,label = "", labelWidth = 23, entryList = [], entryWidth = 30, extra = "") :
    s = ""
    s += "\n"+label.ljust(labelWidth)+" & "+" & ".join([self.toString(entry).ljust(entryWidth) for entry in entryList])+r" \\ %s"%extra
    return s 
  
  def Latex_Table(self,Datanumbers,MCmuon,MCHad,Trans_Factor,rows = []): 
      s  = r'''\begin{table}[ht!]'''
      s += "\n\caption{Muon Sample Predictions %s fb$^{-1}$}"% a.Lumo
      s += "\n\label{tab:results-W}"
      s += "\n\centering"
      s += "\n"+r'''\footnotesize'''
      s += "\n\\begin{tabular}{ |c|c|c|c|c| }"
      s += "\n\hline"
      fullBins = list(LatexTitleEntries) + ["$\infty$"] 
      for subTable in range(2) :
          start = 0 + subTable*len(fullBins)/2
          stop = 1 + (1+subTable)*len(fullBins)/2
          indices = range(start,stop-1)[:len(fullBins)/2]
          bins = fullBins[start:stop]
      	  s += self.oneRow(label ="\scalht Bin (GeV)", entryList = [("%s--%s"%(l, u)) for l,u in zip(bins[:-1], bins[1:])], extra = "[0.5ex]")
          for row in rows:
          	s += self.oneRow(label = row["label"], entryList = [row["entryFunc"][i] for i in indices])
      s += "\n\hline"
      s += "\n\end{tabluar}"
      s += "\n\end{table}"
      f = open('MuonNumbers.tex','w')
      f.write(s)
      f.close()
      print s
      print "\n\n TexTable Output to MuonNumbers.tex"

class Number_Maker(object):
  def __init__(self):
    self.ParseOptions()
    self.File_Input()
    self.Initial_Reader(File_List,MuonMC_List,HadMC_List)
    self.Number_Passer()
    self.Number_Creator() 

  def ParseOptions(self):
    parser = OptionParser()
    parser.add_option("-d","--data",action = "store_true", dest="Data_File",default=True,help="Get Numbers for data folder DataLog. Set To True initially",) 
    parser.add_option("-m","--muonmc",action = "store_true", dest="MC_MuonFile", default=False,help="Get Numbers for Muon MC Analysis",) 
    parser.add_option("-n","--hadmc",action = "store_true", dest="MC_HadFile", default=False,help="Get Numbers for Had MC Analysis",) 
    parser.add_option("-l","--Latex",action = "store_true", dest="Make_Latex", default=False,help="Make Latex Table",)
    parser.add_option("-t","--Ted",action = "store_true", dest="Make_Ted", default=False,help="Make Ted's Number Format",) 
    (self.options,self.args) = parser.parse_args()
     
  def File_Input(self):
    if self.options.Data_File is True:
      for file in glob.glob('DataLog/*.log'):
          self.f = open(file, "r")
          File_List.append(self.f)

    if self.options.MC_MuonFile is True or self.options.MC_HadFile is True:
      self.ScaleFactor = raw_input("How much luminosity to scale to (fb)? ... \n")
      self.Lumo = self.ScaleFactor
      self.ScaleFactor = float(self.ScaleFactor)*10
    else: 
      self.ScaleFactor = 1 
      self.Lumo = "Unknown"     

    if self.options.MC_MuonFile is True:
      for file in glob.glob('MuonMCLog/*.log'):
          self.f = open(file, "r")
          MuonMC_List.append(self.f)
   
    if self.options.MC_HadFile is True: 
      for file in glob.glob('HadMCLog/*.log'):
          self.f = open(file, "r")
          HadMC_List.append(self.f)

  def Initial_Reader(self,filelist,mumclist,hadmclist): 
    for file in filelist:
      for newline in file.readlines():
        filetext.append(newline)
    
    if self.options.MC_MuonFile is True:
      for file in mumclist:
        for newline in file.readlines():
          MuonMCtext.append(newline)

    if self.options.MC_HadFile is True:
      for file in hadmclist:
        for newline in file.readlines():
          HadMCtext.append(newline)

  def Number_Passer(self):
    if self.options.Data_File is True:
      self.Number_Producer(File_List,numberholder,filetext)

    if self.options.MC_MuonFile is True:
      self.Number_Producer(MuonMC_List,MuonMCnumberholder,MuonMCtext)

    if self.options.MC_HadFile is True:
      self.Number_Producer(HadMC_List,HadMCnumberholder,HadMCtext)

  def Number_Producer(self,filename,numbers,finder):    
    i=0
    for file in filename:
      file.seek(0)
      for line in file.readlines():
        for keynum, key in enumerate(keywords):
          if key in line:
            word =(finder[i+3].split(":")[1])
            numbers[keynum]=numbers[keynum]+float(word.split(",")[0])
        i += 1
      file.close()     

  def Number_Creator(self):
    self.TranslationFactor = []
    print " Cut         NumberData        MuonAnalysisMC      HadAnalysisMC      MC Ratio"    
    for num,j in enumerate(numberholder):
      try: self.TranslationFactor.append(HadMCnumberholder[num]/MuonMCnumberholder[num])
      except ZeroDivisionError: self.TranslationFactor.append(0)
      if num <2:  
          print "{0:7s}    {1:4.0f}               {2:5.2f}                 {3:5.2f}           {4:5.2f}".format(keywords[num], numberholder[num], self.ScaleFactor*MuonMCnumberholder[num], self.ScaleFactor*HadMCnumberholder[num], self.TranslationFactor[num])
      else:
        try:
          numberholder[num] = j - numberholder[num+1]
          MuonMCnumberholder[num] = MuonMCnumberholder[num]-MuonMCnumberholder[num+1]
        except IndexError:
          numberholder[num] = j
          MuonMCnumberholder[num] = MuonMCnumberholder[num]
        print "{0:7s}    {1:4.0f}               {2:5.2f}                 {3:5.2f}           {4:5.2f}".format(keywords[num], numberholder[num], self.ScaleFactor*MuonMCnumberholder[num],self.ScaleFactor*HadMCnumberholder[num], self.TranslationFactor[num])
      HadMCnumberholder[num]=HadMCnumberholder[num]*self.ScaleFactor
      MuonMCnumberholder[num]=MuonMCnumberholder[num]*self.ScaleFactor
      numberholder[num]=int(numberholder[num])

if __name__=="__main__":
  a = Number_Maker()
  b = Table_Maker()
  
 

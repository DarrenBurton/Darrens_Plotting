#!/usr/bin/env python
import itertools
import sys
import os
import errno


keywords =["HT 275 GeV", "HT 325 GeV", "HT 375 GeV","HT 475 GeV","HT 575 GeV", "HT 675 GeV", "HT 775 GeV", "HT 875 GeV"]
filetext = []
numberholder = [0,0,0,0,0,0,0,0]
File_List = []

def File_Input():
  Log_Holder = []
  for args in sys.argv:
    if args == sys.argv[0]: continue
    else : Log_Holder.append(args)
  for file in Log_Holder:
    f = open(file, "r")
    File_List.append(f)
  return File_List

def Initial_Reader(filelist):
  for file in filelist:
    for newline in file.readlines():
      filetext.append(newline)

def Number_Extractor(filelist):
  i=0
  for file in filelist:
    file.seek(0)
    for line in file.readlines():
      for keynum, key in enumerate(keywords):
        if key in line:
          word =(filetext[i+3].split(":")[1])
          numberholder[keynum]=int(word.split(",")[0])
      i += 1
    file.close()    

def Number_Creator():
  for num,j in enumerate(numberholder):
    if num <2:  
        print " Cut %s, Number in bin %s " %(keywords[num], numberholder[num])
    else:
      try:
        numberholder[num] = j - numberholder[num+1]
      except IndexError:
        numberholder[num] = j
      print " Cut %s, Number in bin %s " %(keywords[num], numberholder[num])
  
  print "\n\nDone" 

if __name__=="__main__":
  File_Input()
  Initial_Reader(File_List)
  Number_Extractor(File_List)
  Number_Creator()

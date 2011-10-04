#!/usr/bin/env python
from ROOT import *
import ROOT as r
import logging
import itertools
import sys
import os
import glob # List Files in Directory
import errno

def start_screen():
    print "\n\n\n|============================================================================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|===================   STARTING   PLOTTING     SCRIPT =======================|"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "| XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX |"
    print "|============================================================================|"

def Get_Histo_Names(file):
  
     temp =  r.TFile.Open(file)
     DirKeys = temp.GetListOfKeys()
     Dir_List =[]
     Path_List =[]
     subfolder = []
     foldernames = []
     for key in DirKeys:
       subdirect = temp.FindObjectAny(key.GetName())
       if subdirect.GetName() == "susyTree" : pass      
       else :
        foldernames.append(subdirect.GetName())
        for subkey in subdirect.GetListOfKeys() :
         if subkey.GetName() != "tree":
             Dir_List.append(subkey.GetName())
             Path_List.append("%s/%s" % (subdirect.GetName(),subkey.GetName())) 
             subfolder.append(subdirect.GetName())
     return Dir_List, subfolder, Path_List, foldernames         

def Get_Histo_List(file, subfolder, selected, length, path, **karg ):
  
  if "Funky" in karg:
    print "hi"
  for sub in subfolder:
    temp = r.TFile.Open(file).Get(sub)
    DirKeys = temp.GetListOfKeys()
    histList=[]
    hist_Path=[]
    if "all" in karg:     
      for i in range(0,length):
          for k in (DirKeys[selected[i]].ReadObj()).GetListOfKeys():
              if "optionall" in karg:  
                if "_all" not in k.GetName():continue  
                histList.append(k.GetName())
                hist_Path.append("%s/%s" %(path[i],k.GetName()))
              else: 
                histList.append(k.GetName())
                hist_Path.append("%s/%s" %(path[i],k.GetName()))
    else :
        if "optionall" in karg:
          for k in DirKeys[selected].ReadObj().GetListOfKeys():
            if "_all" not in k.GetName(): continue
            histList.append(k.GetName())
            hist_Path.append("%s/%s" %(path,k.GetName()))
        else:
          for k in DirKeys[selected].ReadObj().GetListOfKeys(): 
            histList.append(k.GetName())
            hist_Path.append("%s/%s" %(path,k.GetName()))

  return histList, hist_Path

#=================================================================================#
#================================ Main Program ===================================#
#=================================================================================#

class DarrenPlots(object):
    def __init__(self, **options):
        self.input_files={}     

        if not "style" in options:
            gROOT.SetStyle("Plain")
        else:
            if options["style"] == "plain":
                gROOT.SetStyle("Plain")
            elif options["style"] == "tdr":
                print " Selecting tdr style"
                r.gROOT.ProcessLine(".L tdrstyle.C")
                r.setTDRStyle()
                r.tdrStyle.SetPadRightMargin(0.06)#tweak

        if "batch" in options:
           self.SetBatch(options["batch"])
        
        start_screen()
                
        print "\n\n\n        |===================================================|"
        for opt in options:
           print "        |Option Selected: %s : %s" % (opt, options[opt]) 
        print "        |===================================================| \n\n"
    
    def SetBatch(self,batch):
        ROOT.gROOT.SetBatch(batch)

class List_Files(object):
  def __init__(self):
    self.File_List = []
    self.Analysis_Picker()
 
  def Analysis_Picker(self):
    self.Analysis_Choices = ["1","2","3","4","Q"]
    self.Option_Names = ["Single","Single","Full","Single"]
    self.is_data = True
    self.is_funky = False
    print " \n      What Type of Plots would you Like to Produce? "
    print "    -------------------------------------------------------------"
    print "    | [1] : Data Only [Takes 1 root file]                       |"
    print "    | [2] : MC Only  [Takes 1 root file]                        |"
    print "    | [3] : Data And MC                                         |"
    print "    | [4] : MultiFolder Plots  [Takes 1 root file]              |"
    print "    |       e.g. Plotting Same Histo From Different Folders     |"
    print "    |       In A Root File.                                     |"
    print "    | [Q] : Quit                                                |"
    print "    -------------------------------------------------------------\n"

    self.Analysis_Choose = raw_input("Please Enter..........")
    Menu_Opt.Quit_Function(self.Analysis_Choose,self.Analysis_Choices)
    Wrong = Menu_Opt.Wrong_Selection(self.Analysis_Choose, self.Analysis_Choices, lambda: self.Analysis_Picker())
    self.plot_type = self.Option_Names[int(self.Analysis_Choose)-1]
    if Wrong == False: 
      if self.Analysis_Choose == "2" or self.Analysis_Choose == "3":
        self.is_data = False
      if self.Analysis_Choose == "3":
        self.data_and_mc = True
      if self.Analysis_Choose == "4":
        self.is_funky = True
        D_or_not = ["Y","N"]
        Repeat = True
        while Repeat == True:
          Data_or_not = raw_input("Is this with Data (Y or N)?\n")
          if Data_or_not == "N":
              self.is_data = False
              Repeat = False
          if Data_or_not == "Y":
              self.is_data = True
              Repeat = False
          elif Data_or_not not in D_or_not :
              print " Wrong Input Try Again "    
      self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky) 

  def Scaling_Function(self, **karg):
        if karg["Scale"] == False:
            Scale_Choice = raw_input("\nHow much Luminosity are you scaling MC to (fb)? ")
        else: Lumo_Choice = raw_input("\n How much Luminosity is this (fb)\n")  
        try:
            if karg["Scale"] == False: 
              self.Scale_Factor = float(Scale_Choice)*1000
              self.Lumo_Factor = float(Scale_Choice)
            else: self.Lumo_Factor = float(Lumo_Choice)
        except ValueError:
            print "\nNumber must be entered you mug. Exiting"
            sys.exit()                
      
  def Check_pass(self,Add_Hist,Name,num):
        if not "P" in Add_Hist:
              self.FILES.append(self.Root_File_List[int(Add_Hist)])
              self.MC_Name.append(Name)
              self.Hist_Colour.append(self.Default_Colours[num])
        else : pass  

  def Multi_File_Checker(self, File_List):
      
      tripper = False
      for num1,i in enumerate(File_List):
         for num2,j in enumerate(File_List):
            if num1 == num2 or num2 > num1:
                pass
            elif num1 != num2 and i == j:
                print "\nYou've Put In the same File Twice. Try Again!"
                self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky)
                tripper = True
                return True
      if tripper != True:
        return False
  def File_Chooser(self, **karg):
      self.Default_Colours = [1,4,7,3,5,46]
      self.Hist_Colour = []
      self.Scale_Factor = 0
      Pick_File = []
      Pick_MC = []
      self.Root_File_List = []
      self.Root_File_Num = ["P"]
      self.FILES = []
      self.MC_Name = []
      self.Multiple_Folders = False
      self.Scaling_Function(Scale = karg["Data"] )
      Progress = None
      if Progress == None:
        print "\n    Select Root File " 
        print "   |==========================================|"
        print "   | Root Files in this directory             |"
        print "   |==========================================|"
        for num,file in enumerate(glob.glob('*.root')):
            print "   || %s || %s" %(num, file)
            self.Root_File_List.append(file)
            self.Root_File_Num.append(num)
        print "   |==========================================|"  
      
        if karg["Type"] == "Single":
          Pick_File = raw_input("Which do you want to use..... ")
          Progress = Menu_Opt.Wrong_Selection(Pick_File, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))
          if Progress == False:
              self.FILES.append(self.Root_File_List[int(Pick_File)])
              self.MC_Name = ["Data"] 
        print " Moving On To Plot Selection "       
        self.Hist_Colour = self.Default_Colours
        if karg["addition"] == True:
          self.Multiple_Folders = True
        if karg["Type"] == "Full":
          Pick_File = raw_input("Pick Data File.... ")
          self.Hist_Colour.append(self.Default_Colours[0])
          Progress = Menu_Opt.Wrong_Selection(Pick_File, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))
          if Progress == False:
              self.FILES.append(self.Root_File_List[int(Pick_File)])
              self.MC_Name.append("Data")
              Pick_Combined_Individual = ["1","2"]
              print "\n   Pick Combined MC or Individual (SM & QCD)"
              print "   --------------------------------------------"
              print "   |  1  = Combined                           |"
              print "   |  2  = Individual                         |"
              print "   --------------------------------------------\n"
              Pick_MC = raw_input("Enter Now ... ")
              Progress = Menu_Opt.Wrong_Selection(Pick_MC, Pick_Combined_Individual, lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
          if Pick_MC == "1":
              self.Pick_Combined = raw_input("Choose Combined MC File ")
              self.Check_pass(self.Pick_Combined, "MC",1)
              Progress = Menu_Opt.Wrong_Selection(self.Pick_Combined, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
              Progress = self.Multi_File_Checker(self.FILES)
          if Pick_MC == "2":
              print "If you dont want to add the File type P = Pass"
              self.Pick_QCD = raw_input("Choose QCD File... ")
              Progress = Menu_Opt.Wrong_Selection(self.Pick_QCD, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
              self.Check_pass(self.Pick_QCD, "QCD",2)
              self.Pick_WJets = raw_input("Choose WJets File... ")
              Progress = Menu_Opt.Wrong_Selection(self.Pick_WJets, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
              self.Check_pass(self.Pick_WJets, "WJets",3)
              self.Pick_ZJets = raw_input("Choose ZJets File... ")
              Progress = Menu_Opt.Wrong_Selection(self.Pick_ZJets, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
              self.Check_pass(self.Pick_ZJets, "Z inv",4)
              self.Pick_TTbar = raw_input("Choose TTbar File... ")
              Progress = Menu_Opt.Wrong_Selection(self.Pick_TTbar, str(self.Root_File_Num), lambda: self.File_Chooser(Type = self.plot_type, Data = self.is_data, addition = self.is_funky))    
              self.Check_pass(self.Pick_TTbar, "TTbar",5)
              Progress = self.Multi_File_Checker(self.FILES)
          if Progress == False:
              print " \n   You Have Selected Files "
              print "   ---------------------------"
              for name, i in enumerate(self.FILES):
                  print "    %s | %s" % (self.MC_Name[name],i)
              print "   ---------------------------\n"
              print "    Moving On To Plot Selection "          

class Menu_Choices(object):

    def Wrong_Selection(self,Action_Name,Input_List,Function, **karg):
        if "list" in karg :
            for k in Action_Name :
                if str(k) not in Input_List:
                    print "\n\n\nJog on Mate, thats not one of the options is it son?"
                    print "Ok Have another go. I will not ask you again. \n\n\n" 
                    Function()
                    if "plot_test" in karg:
                      self.complete = False
                      continue
                    else:
                      sys.exit()       
        else:
          if  Action_Name not in Input_List :
              print "\n\n\nJog on Mate, thats not one of the options is it son?"
              print "Ok Have another go. I will not ask you again. \n\n\n" 
              Function()
              return True
          else : return False

    def Return_Main(self,Action_Name, **karg):
        if Action_Name == "M" :
          print "\n\nReturning to Main Screen\n"
          b = PlotSelector(a.FILES[0], Funky=a.Multiple_Folders) 

    def Quit_Function(self,Action_Name,Input_List):

      if Action_Name == "Q": 
         print " \n\n   Alright Cya!"
         sys.exit()
      else : pass    

class PlotCreator(object):
    def __init__(self, file_list, hist_list, folder_list, **options):
        self.file_list = file_list
        self.hist_list = hist_list
        self.folder_list = folder_list
        self.options = options
        self.Plot_Splash_Screen()
        self.Output_Choice()
        self.Plot_Options()        
    
    def Plot_Splash_Screen(self):
        print "\n\n    ============================================="
        print "    ============================================="
        print "    ============== In Plot Maker ================"
        print "    ============================================="
        print "    =============================================\n\n"
    
    def Output_Choice(self):
        print " Choose Your OutPut Directory....."
        self.Out_dir = []
        self.Out_dir = raw_input ("Enter Now... \n ")
        try:
          os.makedirs(self.Out_dir)
          print " \nMaking Directory ::: %s :::\n\n " % self.Out_dir
        except OSError as exc: # Python >2.5
          if exc.errno == errno.EEXIST:
            print "\n Directory ::: %s ::: already exists. Still outputing to directory. \n " % self.Out_dir
            pass
          else: 
            print "Cannot Make %s try again" % self.Out_dir
            Output_Choice()

    def Plot_Options(self):

        tot_length = len(self.hist_list)
        self.OPTION_HOLDER = []
        for i in range (0,tot_length):
          self.OPTION_HOLDER.append("Empty")
        Plotter_Options = ["M","Q","S","A"]
        Plotter_Splitter = []
        Hist_Length = len(self.hist_list)-1
        self.To_Options_Number = []
        self.To_Options_Plot_Names = []
        print "\n\n\n   |===============================================================|"
        print "   |Histo to be Plotted are                                        |"
        print "   |===============================================================|"
        for num,his in enumerate(self.hist_list):
            print "   | %s |   " %  num, his  
            Plotter_Options.append(str(num))
        print "   |=================================================================|"
        print "   | Ok. How would you like to make these plots?                     |"
        print "   |-----------------------------------------------------------------|"
        print "   | S = Quick Plot                                                   "
        print "   |     [Default (Colours,Legend), Data Drawn As Points]             "
        print "   | 0 - {0:-3d} = To Pick Options For Specific Plots                 ".format(Hist_Length) 
        print "   | A = Choose Options To Apply For All Plots                        "
        print "   | Q = Quit                                                         "
        print "   | M = Back To Main Page                                            "
        print "   |=================================================================|"
        Plotter_Options_Choice = raw_input ("\n Enter Now.....")
        self.Plotter_Splitter = [ s.strip() for s in Plotter_Options_Choice.split(",")]  
        Menu_Opt.Quit_Function(Plotter_Options_Choice,Plotter_Options)
        Menu_Opt.Return_Main(Plotter_Options_Choice)
        Menu_Opt.Wrong_Selection(self.Plotter_Splitter, Plotter_Options, lambda: self.Plot_Options(), list = True)
        
        if Plotter_Options_Choice == "S":
            self.Plot_Producer()

        if Plotter_Options_Choice == "A":
            print "\n\n Options Choosen will apply to all Histos in List\n\n"
            for num,his in enumerate(self.hist_list):
              self.To_Options_Number.append(num)
              self.To_Options_Plot_Names.append(his)
            self.Plotting_Option_Menu(self.To_Options_Number,self.To_Options_Plot_Names,all=True)
 
        elif "M" not in self.Plotter_Splitter:
            print "\n\n   You've selected the following histos"
            print "   ========================================="
            for l in self.Plotter_Splitter:
                print "   %s" %l , self.hist_list[int(l)]
                self.To_Options_Number.append(l)
                self.To_Options_Plot_Names.append(self.hist_list[int(l)])
            print "   =========================================\n\n"   
            self.Plotting_Option_Menu(self.To_Options_Number,self.To_Options_Plot_Names)
   
    def Plotting_Option_Menu(self,Option_List, Plot_Names, **karg):
        self.Plot_Names = Plot_Names
        tot_length = len(self.hist_list)
        self.OPTION_HOLDER = []
        for i in range (0,tot_length):
          self.OPTION_HOLDER.append("Empty")
        if "all" in karg:
            print " \nSelect Options for All Histograms"
            for i in self.Plot_Names:
              print i
            self.Individual_option_holder = []  
            self.Option_Chooser(self.Plot_Names,option_all= True)
            for num,y in enumerate(self.hist_list):
              self.OPTION_HOLDER[num] = self.Individual_option_holder
            self.Plot_Producer()
            
        else:
            for l, k in enumerate(Option_List):
                self.current_plot = l
                self.Individual_option_holder = []
                print "Select Options for histo %s" %self.Plot_Names[l]
                self.Option_Chooser(self.Plot_Names[l])    
                self.OPTION_HOLDER[int(k)] = self.Individual_option_holder
            self.Plot_Producer()
        

    def Option_Chooser(self, plot_list, **karg):
        self.complete = True
        self.Option_Listings = ["P","0","1","2","3","4","5"]
        self.Funky_Opts = ["3","4","5"]
        print "============================================"
        print "|  [0] - Set Log-Scale                     |"
        print "|  [1] - Set X-axis Scale                  |"
        print "|  [2] - Set Y-axis Scale                  |"
        print "|  [3] - Stack Histos (For Data/MC only) * |"
        print "|  [4] - Fill Histogram *                  |"
        print "|  [5] - Change Plot Colours/Legend Name  *|"
        print "|  [P] - Pass                              |"
        print "|  [Q] - Quit                              |"
        print "|  [M] - Return to Plot Options            |"
        print "============================================"
        print " * Means Not Applicable to Option 4"
        
        self.Opt_Picker = raw_input("\n Choose One ... ")
        self.Opt_Splitter = [ s.strip() for s in self.Opt_Picker.split(",")]  
        Menu_Opt.Quit_Function(self.Opt_Picker,self.Option_Listings)
        its_funky = False
        if self.options["Funky"] == True:
          for p in self.Opt_Splitter:
            if p in self.Funky_Opts:
              Return_To_Menu = True
            else: Return_To_Menu = False  
          if Return_To_Menu == True:
              print " Selected Option Not available to this Histogram. Select again"
              self.complete = True
              its_funky = True
              if "option_all" in karg: self.Option_Chooser(self.Plot_Names,option_all = True)
              else: self.Option_Chooser(self.Plot_Names[self.current_plot])
        if self.Opt_Picker == "P" :
          print "Passing On Options for this Histogram. Move to next Histogram\n"
          self.complete = False
        if self.Opt_Picker == "M" :
          print "\n\nReturning to Plot Options\n"
          self.Plot_Options()
        if "option_all" in karg:
          Menu_Opt.Wrong_Selection(self.Opt_Splitter, self.Option_Listings, lambda: self.Option_Chooser(self.Plot_Names, option_all = True), plt_test = True, list = True)
        else :
          Menu_Opt.Wrong_Selection(self.Opt_Splitter, self.Option_Listings, lambda: self.Option_Chooser(self.Plot_Names[self.current_plot]), plot_test = True, list = True)
        if its_funky == False:
          if self.complete == True:
            if "0" in self.Opt_Splitter:
              self.Repeater = True
              Log_Y_Menu = ["1","0"]
              while self.Repeater == True:
                  Log_Y = raw_input("Set Log Y  (1 or 0)... ")
                  if Log_Y in Log_Y_Menu: 
                    self.Repeater = False
                    if Log_Y == "1":  self.Individual_option_holder.append("Log_or_not|SetLogy|True")                   
                    else : pass
                  else : print "Wrong Input Try Again"         
              self.complete = False
            if "1" in self.Opt_Splitter:
              self.Repeater = True
              while self.Repeater == True:
                  self.Repeater = False
                  X_axis_input = raw_input("Set X Range (Low,High) .... ")
                  X_Splitter = [ s.strip() for s in X_axis_input.split(",")] 
                  self.Num_Checker(X_Splitter,2,X_Splitter[0],X_Splitter[1])       
                  if self.Repeater ==False:
                    x,y = float(X_Splitter[0]), float(X_Splitter[1]) 
                    self.Individual_option_holder.append("X_Axis|SetAxisRange|%f,%f" %(x,y))                
                    self.Repeater = False         
              self.complete = False           
            if "2" in self.Opt_Splitter:
              self.Repeater = True
              while self.Repeater == True:          
                  self.Repeater = False
                  Y_axis_input = raw_input("Set Y Range (Low,High) .... ")
                  Y_Splitter = [ s.strip() for s in Y_axis_input.split(",")]  
                  self.Num_Checker(Y_Splitter,2,Y_Splitter[0],Y_Splitter[1])
                  if self.Repeater ==False:
                    x,y = float(Y_Splitter[0]), float(Y_Splitter[1]) 
                    self.Individual_option_holder.append("Y_Axis|SetAxisRange|%f,%f" %(x,y))                        
              self.complete = False 
            if "3" in self.Opt_Splitter:
                self.Repeater = True
                while self.Repeater == True:
                  self.StackHolder = []
                  print "===================================="
                  for i in range (0,len(self.file_list)):
                    print "%s  | %s " %(i,a.MC_Name[i])
                  print "===================================="  
                  Stack_Histo_Input = raw_input("Which Histos do you want to stack?")
                  Stack_Histo_Splitter = [s.strip() for s in Stack_Histo_Input.split(",")]
                  try:
                    print "\nStacking\n"
                    for l in Stack_Histo_Splitter:
                      print " %s | %s" %(l, a.MC_Name[int(l)])
                      self.StackHolder.append(int(l))
                    print "========================"   
                    self.Repeater = False
                  except ValueError or IndexError:
                    print "Bad Input Try Again"
                    self.Repeater = True
                self.Individual_option_holder.append("Stack_It|NA|NA")
                self.complete = False  
            if "4" in self.Opt_Splitter:
              self.Repeater = True
              while self.Repeater == True:
                  self.FillHolder = []
                  print "===================================="
                  for i in range (0,len(self.file_list)):
                    print "%s  | %s " %(i,a.MC_Name[i])
                  print "===================================="  
                  Fill_Histo_Input = raw_input('Which Histos would you like to Fill?')
                  Fill_Histo_Splitter = [s.strip() for s in Fill_Histo_Input.split(",")]
                  try:
                    print "Filling"
                    for l in Fill_Histo_Splitter:
                      print " %s | %s" %(l, a.MC_Name[int(l)])
                      self.FillHolder.append(int(l))
                    print "==========================="  
                    self.Repeater = False
                  except ValueError or IndexError:
                    print "Bad Input Try Again"
                    self.Repeater = True
              self.Individual_option_holder.append("Fill_It|NA|NA") 
              self.complete = False      
            if "5" in self.Opt_Splitter:
              self.Repeater = True
              while self.Repeater == True:
                Change_List = []
                Number_List = []
                print "================================"
                print "=Num=== Name ====== Colour ====="
                for num,i in enumerate(a.MC_Name):
                  print "  %s |  %8s    |  %s  " %(num, i, a.Hist_Colour[num])
                  Number_List.append(num)
                Plot_Change_Input = raw_input("\n What Num do you want to change? \n")  
                Plot_Change_Splitter = [s.strip() for s in Plot_Change_Input.split(",")]
                for choice in Plot_Change_Splitter:
                  Change_List.append(choice)
                  if int(choice) not in Number_List:
                    print " You've selected a number not in the list. Do it again"
                    self.Repeater = True
                  else : self.Repeater = False  
                Change_Selector = ["N","C","B"]
                if self.Repeater == False:
                  for j in Change_List:
                    print "Ok what do you want to change for %s \n" %j
                    Changing_Time_Input = raw_input("Enter N - Name, C - Colour, B - Both\n")
                    try:
                      self.Repeater = False
                      if Changing_Time_Input == "N":
                        Name_Change_Input = raw_input("Change name to what?\n")
                        a.MC_Name[int(j)] = Name_Change_Input
                      if Changing_Time_Input == "C":
                        Colour_Change_Input = raw_input("Change colour to what?\n")
                        a.Hist_Colour[int(j)] = int(Colour_Change_Input)
                      if Changing_Time_Input == "B":
                        Name_Change_Input = raw_input("Change name to what?\n")
                        a.MC_Name[int(j)] = Name_Change_Input
                        Colour_Change_Input = raw_input("Change colour to what?\n")
                        a.Hist_Colour[int(j)] = int(Colour_Change_Input)
                      elif Changing_Time_Input not in Change_Selector : 
                        print "Incorrect Option Selected\n\n"
                        self.Repeater = True   
                    except ValueError or IndexError:
                        print "Bad Input Try Again"
                        self.Repeater = True
                self.complete = False
          return
          
    def Num_Checker(self,CheckList,maxlength,To_Checkone,To_Checktwo):
      try:
        float(To_Checkone)
        float(To_Checktwo)
        if len(CheckList) > int(maxlength):
          print "Too many inputs Try again"
          self.Repeater = True
        if float(To_Checkone) > float(To_Checktwo):
          print "Range set wrongly Try again"
          self.Repeater = True
      except ValueError:
        print "Non-Number Inputted Try Again"
        self.Repeater = True

    def Option_File(self, Apply_To_Hist, Options_Passed):
        if "Empty" in Options_Passed:
            pass
        else :
          for opt in Options_Passed:
            multi_argument = []
            special_opt = opt.split('|')[0]
            split_opt = opt.split('|')[1]
            variable = opt.split('|')[2]
            if len(variable.split(',')) == 1:
              test = bool(variable)
            else:
              for j in range(0, len(variable.split(','))):
                multi_argument.append(float(variable.split(',')[j]))
              if special_opt == "Y_Axis":
                multi_argument.append("y")
              if special_opt == "X_Axis":
                multi_argument.append("x")
            if hasattr(Apply_To_Hist,split_opt):
              if len(variable.split(','))  == 1:
                  applyer = getattr(Apply_To_Hist,split_opt)
                  applyer(test)
              else:
                  applyer = getattr(Apply_To_Hist,split_opt)
                  if len(multi_argument) == 2:
                  #applyer(multi_argument[i] for i,j in enumerate(multi_argument))
                    applyer(multi_argument[0],multi_argument[1])
                  if len(multi_argument) == 3:
                    applyer(multi_argument[0],multi_argument[1],multi_argument[2])

    def For_Funky(self): 
       self.new_hist_list = []
       for fnum,k in enumerate(self.hist_list):
          for j in self.folder_list:
            joined = j+"/"+k
            self.new_hist_list.append(joined)
       self.hist_list = self.new_hist_list
      
    def Funky_Plotter(self):
        
        self.Funky_FolderList = Get_Histo_Names(a.FILES[0])[3]
        Funky_Legends = []
        for i in self.Funky_FolderList:
          Funky_Legend_Input = raw_input("What Legend entry do you want for %s?\n" % i)
          Funky_Legends.append(Funky_Legend_Input)
        option_counter = 0  
        for num in range(0,len(self.HIST_GROUPED),len(self.folder_list)):
            lower = num
            higher = lower + len(self.folder_list)
            print "\n Making Histogram %s" % self.HIST_NAMED[num]
            c1 = r.TCanvas("canvas"+str(num),"canname"+str(num),1200,1200)     
            c1.cd(1)
            self.Option_File(c1,self.OPTION_HOLDER[option_counter])
            if self.options["MC_Scale"] != 0: self.norm  = self.options["MC_Scale"]/100
            for plot in range(lower,higher,1):
              if plot == lower:
                self.Legend_Maker()
                colour_changer = 0
                First = self.HIST_GROUPED[lower][0]
                First.Scale(self.norm)
                self.Option_File(First,self.OPTION_HOLDER[option_counter])
                self.leg.AddEntry(First,Funky_Legends[0],"L")
                print " Drawing %s " %self.HIST_GROUPED[lower][0]
                if hasattr(First,"SetLineColor"):
                      colour_applyer = getattr(First,"SetLineColor") 
                      colour_applyer(a.Hist_Colour[colour_changer])
                First.Draw("p")
              else:
                print " Drawing %s" %self.HIST_GROUPED[plot][0]
                next = self.HIST_GROUPED[plot][0]
                next.Scale(self.norm)
                self.leg.AddEntry(next,Funky_Legends[colour_changer],"L")
                if hasattr(next,"SetLineColor"):
                      colour_applyer = getattr(next,"SetLineColor") 
                      colour_applyer(a.Hist_Colour[colour_changer])
                next.Draw("samehist")
              colour_changer += 1 
            self.leg.Draw("same")  
            c1.SaveAs("%s/%s.jpg"% (self.Out_dir, self.HIST_NAMED[num]))
            print "Done. On To the Next One."
            self.Webpage_List.append("%s.jpg"% self.HIST_NAMED[num])
            option_counter += 1
        if self.webpage_maker == True:
          self.HTMLMaker(self.Out_dir, self.Webpage_List) 
        print "\n\nOk All Done!!!!"  
        sys.exit() 
    
    def HTML_Maker(self,Outputdir,Plot_Names):
      print "\n       ================================" 
      print "       ======== Making Webpage ========"
      print "       ********************************\n\n"
      HTMLfile = open(''+Outputdir+'/Plots.html','w')
      HTMLfile.write('Directory : '+Outputdir+' \n')
      HTMLfile.write('<br>\n')
      for hist in Plot_Names:
        HTMLfile.write('<div style="float: left">')
        HTMLfile.write('<a href="'+hist+'">')
        HTMLfile.write('<embed src= \"'+hist+'\", TITLE ="'+hist+'" width=480 height=365></a></div>')

    def Plot_Producer(self):
        if self.options["Funky"] == True: self.For_Funky()
        self.HIST_GROUPED = []
        self.HIST_NAMED = []
        for i in self.hist_list:
           self.file_name_strip = [j.strip() for j in i.split("/")]
           str = "_"
           self.file_name_join = str.join(self.file_name_strip)
           self.histomizer = []
           for fnum,k in enumerate(self.file_list):
                a = r.TFile.Open(self.file_list[fnum]).Get(i) #open the file
                self.histomizer.append(a)
           self.HIST_GROUPED.append(self.histomizer)
           self.HIST_NAMED.append(self.file_name_join)
          
        self.Plot_Ending()

    def Legend_Maker(self):
        self.leg = r.TLegend(0.70,0.75,0.93,0.9)
        title = "\int L dt = %s fb^{-1}" % a.Lumo_Factor
        self.leg.SetHeader(title)
        self.leg.SetShadowColor(0)
        self.leg.SetBorderSize(0)
        self.leg.SetFillColor(0)
        self.leg.SetLineColor(0)
      
    def Plot_Ending(self):
        self.norm = 1
        self.Webpage_List = []
        Produce_Webpage_Input = raw_input("\n Do you want to make this a webpage? (Y or N)\n")
        if "Y" in Produce_Webpage_Input: self.webpage_maker = True
        else : self.webpage_maker = False
        if self.options["Funky"] == True:
            self.Funky_Plotter()
            sys.exit()
        for hist_num,j in enumerate(self.HIST_GROUPED):
            Stacked_Histo = r.THStack()
            self.Legend_Maker()
            print "\n Making Histogram %s" % self.HIST_NAMED[hist_num]
            c1 = r.TCanvas("canvas"+str(hist_num),"canname"+str(hist_num),1200,1200) 
            self.Option_File(c1,self.OPTION_HOLDER[hist_num])
            c1.cd(1)
            for l in range (0,len(self.file_list)): 
                if self.options["MC_Scale"] != 0:
                  if len(self.file_list) > 1 and l ==0:
                      self.norm = 1
                  else:      
                      self.norm  = self.options["MC_Scale"]/100
                if l == 0:
                    First = self.HIST_GROUPED[hist_num][0]
                    First.Scale(self.norm)
                    self.Option_File(First,self.OPTION_HOLDER[hist_num])
                    First.Draw("P")
                    self.leg.AddEntry(First,a.MC_Name[l],"L")
                else:
                    p = self.HIST_GROUPED[hist_num][l]
                    p.Scale(self.norm)
                    p.SetLineWidth(3)
                    self.leg.AddEntry(p,a.MC_Name[l],"L")
                    if hasattr(p,"SetLineColor"):
                       colour_applyer = getattr(p,"SetLineColor") 
                       colour_applyer(a.Hist_Colour[l])
                    if "Fill_It|NA|NA" in self.OPTION_HOLDER[hist_num]:
                      if l in self.FillHolder:
                        p.SetFillColor(a.Hist_Colour[l])
                    if "Stack_It|NA|NA" in self.OPTION_HOLDER[hist_num]:
                      if l in self.StackHolder:
                        Stacked_Histo.Add(p)
                      else:
                        p.Draw("histsame")
                    else:
                       p.Draw("histsame")  
            Stacked_Histo.Draw("histsame")
            First.Draw("Psame")
            self.leg.Draw("same")
            c1.SaveAs("%s/%s.jpg"% (self.Out_dir, self.HIST_NAMED[hist_num]))
            self.Webpage_List.append("%s.jpg" % self.HIST_NAMED[hist_num])
            print "Done. On To the Next One."
        if self.webpage_maker == True:
          self.HTML_Maker(self.Out_dir,self.Webpage_List)
        print "\n\nOk All Done!!!"    
        sys.exit() 

class PlotSelector(object):
    def __init__(self, name, **options):
        
        self.funky = False
        self.options=options
        self.name = name
        self._options={}
        self.To_Plotter =[]
        self.Folder_Choice()
        self.Folder_Action()        

    def Plotting_Point(self):

      Plot_Selector = ["Q","A","M"]
      Confirm_List = ["Y","N"]
      Repeat = True
      self.plot_inputs=[]
      self.To_Plotter=[]
      H_Length = len(self.Hist_In_Folder) - 1
      for i in range (0,len(self.Hist_In_Folder)):
        Plot_Selector.append(str(i))
      print "\n\n   |========================================================|"
      print "   | Do you to make All Plots? Or certain selected Plots?   |"
      print "   |--------------------------------------------------------|"
      print "   | A = For All Plots                                      |"
      print "   | 0 - {0:-3d} = To pick Specific Histos                    |".format(H_Length) 
      print "   | Q = Quit                                               |"
      print "   | M = Back to main page                                  |"
      print "   |========================================================|"
      
      Selection = raw_input (" Enter Now...")
      self.plot_inputs= [ s.strip() for s in Selection.split(",")]  
      Menu_Opt.Quit_Function(Selection,Plot_Selector) 
      Menu_Opt.Return_Main(Selection)
      Menu_Opt.Wrong_Selection(self.plot_inputs, Plot_Selector, lambda: self.Folder_Action(), list = True)
      
      if Selection == "A":
        print "\n\nPassing onto Plotting op\n\n"
        print "   ========================================="
        for l in self.Path_To_Hist:
            print "   %s" %l    
        print "   ========================================="
        self.To_Plotter = self.Path_To_Hist
        PlotCreator(a.FILES,self.To_Plotter, self.foldernames, MC_Scale = a.Scale_Factor, Funky = a.Multiple_Folders)
        return self.To_Plotter

      elif "M" not in self.plot_inputs:
          print "\n\n   You've selected just Histos... "
          print "   ========================================="
          for l in self.plot_inputs:
              print "   %s" %l , self.Path_To_Hist[int(l)]
              self.To_Plotter.append(self.Path_To_Hist[int(l)])
          print "   ========================================="
        
          while Repeat == True:
              Confirmation = raw_input (" Confirm Y or N ....\n")
              if Confirmation == "Y":
                  Repeat = False
                  print "\nPassing to Plotting Op"
                  PlotCreator(a.FILES,self.To_Plotter, self.foldernames, MC_Scale =a.Scale_Factor, Funky = a.Multiple_Folders)
                  return self.To_Plotter
              if Confirmation == "N":
                  Repeat = False
                  self.Plotting_Point()   
              if not Confirmation in Confirm_List:
                  print "Wrong Input Try Again\n"
                  Repeat = True

      
    def Folder_Choice(self):

        self.FolderList = Get_Histo_Names(self.name)[0]
        self.subfolder  = Get_Histo_Names(self.name)[1]
        self.Path_List  = Get_Histo_Names(self.name)[2]
        self.foldernames = Get_Histo_Names(self.name)[3]
        self.F_Length = len(self.FolderList) - 1
        Action_List = ["A","Q"]
        previous_holder = self.subfolder[0]
        counter = 0
        self.dir_passer = []
        print "\n\n\n   |===================================================|"
        print "   |Directories in ROOT File :: %s are        " %self.name
        print "   |===================================================|"
        if self.options["Funky"] == True:
            self.funky = True
            self.F_Length = len(self.FolderList)/len(self.foldernames) - 1
            print "   | Analysis Option 4 Chosen : One Directory is       |" 
            print "   | being shown only                                  |"
            print "   |===================================================|"
        for num,dir in enumerate(self.FolderList):
            folder_holder = self.subfolder[num]
            if previous_holder != self.subfolder[num]:
              if self.options["Funky"] == True: break  
              counter = 0
              self.dir_passer.append(counter)
            else:
              self.dir_passer.append(counter)
              counter += 1 
            print "   |Subfolder ::: % s || % s | %s  " %  (self.subfolder[num],num, dir)
            previous_holder = folder_holder
            Action_List.append(str(num))
        print "   |===================================================|"
        print "   | Make Plots from?                                  |"
        print "   |===================================================|"
        print "   | Choose Number [0-%s] for directory                 | "% self.F_Length
        print "   | Choose 'A' for all directories                    |"
        print "   | Choose 'Q' to Quit                                |"
        print "   |===================================================|"
        self.action = raw_input ("\n\nEnter Now ")
        Menu_Opt.Wrong_Selection(self.action,Action_List, lambda: self.Folder_Choice())
        Menu_Opt.Quit_Function(self.action,Action_List)
        
    def Folder_Action(self):  

        Choose_all = ["Y","N"]
        all_statement = False
        length_passer = 0
        action_passer = []
        self.subfolder_choice = []
        write_dir = True
         
        if self.action == "A" :
            print "   |===========================================|"
            print "    Ok Selecting all."
            print "   |===========================================|"
            all_statement = True
            length_passer= len(self.FolderList)
            self.subfolder_choice = self.subfolder
            self.Path_passer=self.Path_List
            action_passer = self.dir_passer
        else :  
            length_passer = self.F_Length
            self.subfolder_choice.append(self.subfolder[int(self.action)])
            self.Single_Path_passer=self.Path_List[int(self.action)] 
            action_passer = self.dir_passer[int(self.action)]
        self.optionall = raw_input (" \n Do you want to display just '_all' histograms? (Y or N)\n")
        print "   |================================================|"
        if not self.optionall in Choose_all:
              print "\n\nIncorrect Input Try again \n\n\n"
              self.Folder_Action()
        elif self.optionall == "N":
              print "   Selecting every histogram."
              print "   |================================================|"
              if all_statement == True:
                  self.Hist_In_Folder = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Path_List, all=all_statement)[0]
                  self.Path_To_Hist = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Path_List, all=all_statement)[1]          
              else :
                  self.Hist_In_Folder = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Single_Path_passer)[0]  
                  self.Path_To_Hist = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Single_Path_passer)[1]
        elif self.optionall == "Y":
              print "   Selecting just '_all' histograms."
              print "   |================================================|"
              if all_statement == True:
                self.Hist_In_Folder = Get_Histo_List(self.name, self.subfolder_choice, action_passer , length_passer, self.Path_List, all=all_statement, optionall = True)[0]
                self.Path_To_Hist = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Path_List, all=all_statement, optionall = True)[1]
              else:
                self.Hist_In_Folder = Get_Histo_List(self.name, self.subfolder_choice, action_passer , length_passer, self.Single_Path_passer, optionall = True)[0]
                self.Path_To_Hist = Get_Histo_List(self.name, self.subfolder_choice, action_passer, length_passer, self.Single_Path_passer, optionall = True)[1]
        previous_sub_fold = 0 
        for nums, num_hist in enumerate(self.Hist_In_Folder): 
                if all_statement == True:
                    if previous_sub_fold != self.Path_To_Hist[nums].split("/")[0]:
                        print "   |================================================|"
                        print "   |Directory %s" %self.Path_To_Hist[nums].split("/")[0]
                        print "   |================================================|"
                    previous_sub_fold = self.Path_To_Hist[nums].split("/")[0]    
                print "   | %s  | " % nums, num_hist
                print "   |------------------------------------------------|"
        if self.options["Funky"] == True:
            self.new_Path_To_Hist = []
            for i, histo in enumerate(self.Hist_In_Folder):
                path_split = self.Path_To_Hist[i].split("/")[1]
                self.new_Path_To_Hist.append("%s/%s" %(path_split,histo))
            self.Path_To_Hist = self.new_Path_To_Hist

        self.Plotting_Point()

if __name__=="__main__":
   p = DarrenPlots( batch=True, style="tdr")
   Menu_Opt = Menu_Choices()
   a = List_Files()
   b = PlotSelector(a.FILES[0], Funky=a.Multiple_Folders)
   
   

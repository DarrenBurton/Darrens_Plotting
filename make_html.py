import os

BDTtype = ['ada','grad']
names = ['_115','_120','_125','_130','_135','_140','_150']

for bdt in BDTtype:
  allHTMLfile = open('SigInterp/'+bdt+'/all.html','w')
  for masspoint in names:
    outHTMLfile = open('SigInterp/'+bdt+'/'+masspoint+'/'+bdt+masspoint+'.html','w')
    
    outHTMLfile.write('BDT type: \n')
    outHTMLfile.write('<a href=\"../../ada/'+masspoint+'/ada'+masspoint+'.html\">ada</a>\n')
    outHTMLfile.write('<a href=\"../../grad/'+masspoint+'/grad'+masspoint+'.html\">grad</a>\n')
    outHTMLfile.write('<br>\n')

    outHTMLfile.write('Trained at: \n')
    for masses in names:
      outHTMLfile.write('<a href=\"../../'+bdt+'/'+masses+'/'+bdt+masses+'.html\">'+masses+'</a>\n')
    outHTMLfile.write('<a href=\"../all.html\">all</a>\n')
    outHTMLfile.write('<br>\n')
    
    if masspoint=="_115":
      allHTMLfile.write('BDT type: \n')
      allHTMLfile.write('<a href=\"../ada/all.html\">ada</a>\n')
      allHTMLfile.write('<a href=\"../grad/all.html\">grad</a>\n')
      allHTMLfile.write('<br>\n')

      allHTMLfile.write('Trained at: \n')
    
      for masses in names:
        allHTMLfile.write('<a href=\"../'+bdt+'/'+masses+'/'+bdt+masses+'.html\">'+masses+'</a>\n')
      allHTMLfile.write('<a href=\"../'+bdt+'/all.html\">all</a>\n')
      allHTMLfile.write('<br>\n')
    
    for masses in names:
      outHTMLfile.write('<embed src=\"histo'+masses+'.jpg\" width=500 height=375>\n')
      outHTMLfile.write('<embed src=\"frac'+masses+'.jpg\" width=500 height=375>\n')
    outHTMLfile.write('<embed src=\"histo_all_'+bdt+masspoint+'.jpg\" width=500 height=375>\n')
    outHTMLfile.write('<embed src=\"frac_all_'+bdt+masspoint+'.jpg\" width=500 height=375>\n')
    outHTMLfile.write('<embed src=\"graph_'+bdt+masspoint+'.jpg\" width=500 height=375>\n')

    allHTMLfile.write('<embed src=\"'+masspoint+'/frac_all_'+bdt+masspoint+'.jpg\" width=500 height=375>\n')
    allHTMLfile.write('<embed src=\"'+masspoint+'/graph_'+bdt+masspoint+'.jpg\" width=500 height=375>\n')


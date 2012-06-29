#!/usr/bin/env python

import sys
import sfle
import arepa
import os

#CAll: python src/getTaxidsFromChildren.py 197 


###### INPUT
c_inputbug = sys.argv[1]
c_outputfile = sys.argv[2]

###### CONSTANTS required for running this script
c_fileNCBItaxonomy      = sfle.d( arepa.path_arepa(),"GeneMapper", sfle.c_strDirEtc, "NCBItaxonomy.tab") #taxa=root and run taxdump2taxa.py!
###### VARIABLES
c_fileInputTaxa         = sfle.d( arepa.path_repo(), sfle.c_strDirTmp, "taxa" ) 
c_BugChildrenTaxa       = sfle.d( arepa.path_repo(), sfle.c_strDirTmp, "BugChildrenTaxa") 
c_fileTaxdumpTXT        = sfle.d( arepa.path_arepa( ), sfle.c_strDirTmp, "taxdump.txt" ) 
##### EXTERNAL SCRIPTS
c_fileProgTaxdump2Taxa  = sfle.d( arepa.path_arepa( ), sfle.c_strDirSrc, "taxdump2taxa.py" ) 



###### LOCAL FUNCTIONS

#Get bug name of input taxid:
def funcGetBugName (inputbug, fileNCBItaxonomy):
    bug = 0
    for line in open(fileNCBItaxonomy,'r'):
        taxid, species = line.split("\t")
        if (taxid == inputbug):
            bug = species
            break
    return bug

#Write bug name into c_fileInputTaxa so that the external arepa script c_fileProgTaxdump2Taxa can be called:
def funcWriteBugtofile(bug, filename):
    f=open(filename,"w")
    f.write(bug)
    f.close()

#Get all taxids from the bug's children:
def funcGetChildrenTaxids(filename, outputfile):
    f = open(outputfile, "w")
    for line in open(filename,"r"):
        #print (line.split("\t")[0])
        f.write(line.split("\t")[0]+"\n")
    f.close

####### CALLS

bug = funcGetBugName (c_inputbug, c_fileNCBItaxonomy)
print bug
if bug != 0:
    funcWriteBugtofile(bug, c_fileInputTaxa)
    #Call external arepa script to get all taxonomical children of the bug:
    children = sfle.ex([c_fileProgTaxdump2Taxa, c_fileInputTaxa, "<", c_fileTaxdumpTXT,">",c_BugChildrenTaxa ])
    funcGetChildrenTaxids(c_BugChildrenTaxa, c_outputfile)
else:
    print("+++ Error in getTaxidsFromChildren.py : input taxid not found! ")


        

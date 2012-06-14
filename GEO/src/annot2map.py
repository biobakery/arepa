import sfle 
import glob
import csv  

''' parse mapping files '''

astrAnnot = glob.glob("*.annot.gz")
strAnnot  = astrAnnot[0] 

for strLine in open( astrAnnot, "r" ).readlines():
	if strLine ==  

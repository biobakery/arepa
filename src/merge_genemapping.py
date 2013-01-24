'''
merges two or more gene mapping files 
to produce one combined mapping file.
assumes that the mapping files are unique 
and error-free
'''

import sys
import csv 
import sets 

if len(sys.argv[1:]) < 2:
	raise Exception("Usage: merge_genemapping.py <map1.txt> <map2.txt>")


fielIn1 = sys.argv[1]
fileIn2 = sys.argv[2]

csvr1 = csv.reader(open(fileIn1),csv.excel_tab)
csvr2 = csv.reader(open(fileIn2),csv.excel_tab)

aastrDataIn1, aastrDataIn2  = [(x for x in f) for f in [csvr1,csvr2]]
sstrHeader1, sstrHeader2 = set(aastrDataIn1[0]), set(aastrDataIn2[0])

sstrHeaderIntersect = sstrHeader1 & sstrHeader2

aastrDataIn1Zip = zip(*aastrDataIn1)
aastrDataIn2Zip = zip(*aastrDataIn2)

daastrData1 = {x[0]:x[1:] for x in aastrDataIn1Zip}
daastrData2 = {x[0]:x[1:] for x in aastrDataIn2Zip}

daastrDataMod1 = {k:daastrData1[k] for k in sstrHeaderIntersect}
daastrDataMod2 = {k:daastrData2[k] for k in sstrHeaderIntersect}

for strHeader in sstrHeaderIntersect:
	len( set(daastrDataMod1[strHeader]) & set(daastrDataMod2[strHeader]) )

baseline_keys =  

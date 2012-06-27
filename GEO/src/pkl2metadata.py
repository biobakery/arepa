#!/usr/bin/env python 

import arepa 
import csv 
import sys
import metadata 

'''
This script produces 2 tab-delimited tables:
one for the per-experiment metadata and 
one for the per-condition metadata
'''

c_strCurated	= "curated"

if len(sys.argv[1:]) != 3:				
	raise Exception("usage: pkl2metadata.py <ID.pkl> <per-exp.txt> <per-cond.txt>")
 
c_fileIDpkl, c_fileExpTable, c_fileCondTable = sys.argv[1:]	
hashMeta = metadata.open( open( c_fileIDpkl, "r" ) ) 

astrExp, astrCond = filter( lambda k: isinstance(hashMeta.get(k),str or int or float), \
	hashMeta.keys() ), filter( lambda k: isinstance(hashMeta.get(k),list) and \
	k != c_strCurated, hashMeta.keys() ) 

def writeTable( hMeta, astrKeys, outputf, bIter = False ):
	hMeta = {k:hMeta[k] for k in astrKeys}
	csvw = csv.writer( open( outputf, "w" ), csv.excel_tab )
	csvw.writerow( astrKeys )
	if bIter:
		astrHeader = hMeta.get("sample_name") or hMeta.get("")
		#sys.stderr.write( type(astrHeader)  )
		for iSample, strSample in enumerate(astrHeader):
			#for s in astrKeys:
				#sys.stderr.write( str(iSample) + '\n' )
				#sys.stderr.write( '#' + hMeta.get(s)[iSample] + '\n' ) 
			csvw.writerow( map( lambda x: str(x).replace("\n"," "), \
			[hMeta.get(s)[iSample] for s in astrKeys] )) 
	else:
		csvw.writerow( map(lambda x: str(x).replace("\n"," "), \
		[hMeta[k] for k in astrKeys]) )

#write per-experiment table 
writeTable( hashMeta, astrExp, c_fileExpTable, False )
#write per-condition table 
writeTable( hashMeta, astrCond, c_fileCondTable, True )


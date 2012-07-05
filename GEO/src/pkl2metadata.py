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

if not(2 <= len(sys.argv[1:]) <= 3):				
	raise Exception("usage: pkl2metadata.py <ID.pkl> <per-exp.txt> [per-cond.txt]")
 
c_fileIDpkl, c_fileExpTable 	= sys.argv[1:3]
c_fileCondTable		    	= sys.argv[3] if len( sys.argv[1:] ) > 2 else None 

hashMeta = metadata.open( open( c_fileIDpkl, "r" ) ) 

def writeTable( hMeta, astrKeys, outputf, bIter = False ):
	hMeta = {k:hMeta[k] for k in astrKeys}
	csvw = csv.writer( open( outputf, "w" ), csv.excel_tab )
	if bIter:	
		astrHeader = hMeta.get("sample_name") or hMeta.get("")
		_astrKeys = filter(lambda x: hMeta.get(x) != astrHeader,astrKeys)
		csvw.writerow( ["sample_name"] + _astrKeys )
		for iSample, strSample in enumerate(astrHeader):
			csvw.writerow( map( lambda x: str(x).replace("\n"," "), \
			[ strSample ] + [hMeta.get(s)[iSample] for s in \
			_astrKeys] )) 
	else:
		csvw.writerow( astrKeys )
		csvw.writerow( map(lambda x: str(x).replace("\n"," "), \
		[hMeta[k] for k in astrKeys]) )

#write per-experiment table 
astrExp = filter( lambda k: isinstance(hashMeta.get(k),str or int or float), \
	hashMeta.keys() ) 
writeTable( hashMeta, astrExp, c_fileExpTable, False )

#write per-condition table
if c_fileCondTable:
	astrCond = filter( lambda k: isinstance(hashMeta.get(k),list) and \
        k != c_strCurated, hashMeta.keys() )
	writeTable( hashMeta, astrCond, c_fileCondTable, True )


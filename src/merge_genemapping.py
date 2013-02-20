#!/usr/bin/env python
'''
merges two gene mapping files 
to produce one combined mapping file.
assumes that the mapping files are unique 
and error-free
'''

import sys
import csv 
import sets 

def _merge_row( dRow1, dRow2 ):
	'''merge two rows, taken as dictionary objects'''
	astrKeys1, astrKeys2 = dRow1.keys(), dRow2.keys()
	sstrKeyIntersect = (set(astrKeys1) & set(astrKeys2))
	assert( any(sstrKeyIntersect) )
	#for strKey in sstrKeyIntersect:
	#	assert( dRow1[strKey] == dRow2[strKey] )
	for strKey in astrKeys2:
		if not(strKey in astrKeys1):
			dRow1[strKey] = dRow2[strKey]
	return dRow1

def merge( strFile1, strFile2 ):
	dummyOut = [] 

	csvd1 = csv.DictReader(open(fileIn1),delimiter="\t")
	csvd2 = csv.DictReader(open(fileIn2),delimiter="\t")

	adstrDataIn1, adstrDataIn2  = [[x for x in f] for f in [csvd1,csvd2]]
	sstrHeader1, sstrHeader2 = set(adstrDataIn1[0].keys() if adstrDataIn1 else []), set(adstrDataIn2[0].keys() if adstrDataIn2 else [])

	sstrHeaderIntersect = sstrHeader1 & sstrHeader2
	sstrHeaderUnion = sstrHeader1 | sstrHeader2 
	astrHeaderIntersect = list(sstrHeaderIntersect)

	pTemp =  [set(map(lambda x: x[strHeader], adstrDataIn1)) & set(map(lambda x: x[strHeader], adstrDataIn2)) for strHeader in astrHeaderIntersect]

	if adstrDataIn1 and not(adstrDataIn2):
		for dct in adstrDataIn1:
			for item in (sstrHeaderUnion - sstrHeader1):
				dct[item] = ""
			dummyOut.append(dct) 
		return dummyOut 
	elif not(adstrDataIn1) and adstrDataIn2:
		for dct in adstrDataIn2:
			for item in (sstrHeaderUnion - sstrHeader2):
				dct[item] = ""
			dummyOut.append(dct)
		return dummyOut 
	elif not(adstrDataIn1) and not(adstrDataIn2):
		return [{k:"" for k in sstrHeaderUnion}] 
	elif not(sstrHeaderIntersect) or not(pTemp):
		for dct in adstrDataIn1:
                        for item in (sstrHeaderUnion - sstrHeader1):
                                dct[item] = ""
                        dummyOut.append(dct)
		for dct in adstrDataIn2:
                        for item in (sstrHeaderUnion - sstrHeader2):
                                dct[item] = ""
                        dummyOut.append(dct)
                return dummyOut	
	else:
		pMaxHeader = max( [(set(map(lambda x: x[strHeader], adstrDataIn1)) & set(map(lambda x: x[strHeader], adstrDataIn2)), 
			strHeader) for strHeader in astrHeaderIntersect], key=lambda x: len(x[0]) )

		sstrMaxGeneIDs = pMaxHeader[0]
		strMaxHeader = pMaxHeader[1]

		pKeyData1 = {d[strMaxHeader]:d for d in adstrDataIn1}
		pKeyData2 = {d[strMaxHeader]:d for d in adstrDataIn2}

		for strKey in pKeyData1.keys():
			if strKey in sstrMaxGeneIDs:
				if not(strKey in pKeyData2.keys()): 
					continue 
				else:
					dummyOut.append( _merge_row( pKeyData1[strKey], pKeyData2[strKey] ) )
			else:
				for leftover_header in (sstrHeaderUnion - sstrHeader1): 
					pKeyData1[strKey][leftover_header]  = "" 
				dummyOut.append(pKeyData1[strKey])
		for strKey in pKeyData2.keys():
			if not(strKey in sstrMaxGeneIDs):
				for leftoever_header in (sstrHeaderUnion - sstrHeader2):
					pKeyData2[strKey][leftover_header] = ""
				dummyOut.append(pKeyData2[strKey]) 

		return dummyOut 

#Execution 
if len(sys.argv[1:]) < 3:
	raise Exception("Usage: merge_genemapping.py <map1.txt> <map2.txt> <out.txt>")

fileIn1, fileIn2, fileOut  = sys.argv[1:]
if all([fileIn1,fileIn2,fileOut]):
	pMapOut =  merge( fileIn1, fileIn2 ) 

csvw = csv.DictWriter( open(fileOut,"w"), fieldnames=pMapOut[0].keys(), delimiter="\t" )
csvw.writeheader()
csvw.writerows( pMapOut )	

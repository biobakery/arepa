#!/usr/bin/env python 

import arepa 
import csv 
import sys
import pickle
import matrix 
import re 
import types 

#this script produces 2 tab-delimited tables:
#one for the per-experiment metadata and 
#one for the per-condition metadata
 

c_astrStandards 	= ["curated","taxid", "type", "pmid", "platform", "title", "gloss", "channels", "conditions"]
c_hashkeyCurated	= "curated"

 
if len(sys.argv[1:]) != 3:		
	raise Exception("usage: pkl2metadata.py <ID.pkl> <per-exp.txt> <per-cond.txt>")

#Use shared metadata class to do all this 

c_fileIDpkl, c_fileExpTable, c_fileCondTable = sys.argv[1:]	
hashData = pickle.load( open(c_fileIDpkl,"r") ) 

m_missingKey = [] 

def getKeys():
	''' 
	returns uncurated, curated keys 
	'''
	rUncurated = []
	rCurated = hashData[c_hashkeyCurated] 
	for item in hashData.keys():
		if item in rCurated:
			continue 
		else:
			rUncurated.append(item) 
	#make sure that the list of keys are of the correct size 
	assert(len(hashData.keys()) == len(rUncurated) + len(rCurated))	
	return rUncurated, rCurated  

def tryMap( dictionary, keylst ):
	rDict = {}
	for key in keylst:
		try:
			rDict[key] = dictionary[key]
		except KeyError:
			pass 
	return rDict  

def writeTable( dictionary, keys, outfile ):
	'''
	takes in a dictionary, keys, 
	and output file and writes into 
	a column format
	''' 
	dictionary = tryMap( dictionary, keys )
	outMat = matrix.dict2colmat( dict, keys )
	outMat = matrix.stripMat( outMat )
	with open( outfile, "w") as outputf:
		for row in outMat:
			outputf.write("\t".join( row ) + "\n")

#Execute 

#get keys 
uncuratedKeys, curatedKeys = getKeys()
print "The uncuratedKeys are:"
print "\n".join(uncuratedKeys) + "\n"
print "The curatedKeys are:"
print "\n".join(curatedKeys) + "\n"

#write per-experiment table 
writeTable( hashData, uncuratedKeys, c_fileExpTable)
#write per-condition table 
writeTable( hashData, curatedKeys, c_fileCondTable)

if m_missingKey:
	print "The following keys are missing in the metadata:\n", \
		("\n".join(m_missingKey)) 



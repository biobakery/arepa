#!/usr/bin/env python
'''
make gene mapping unique 
for NxM mappings and handle duplicate entries
'''
import sets
import itertools 

def handleDoubleEntries( mat ):
	'''
	gets rid of double entries isomorphic up to permutation;
	make sure to run AFTER makeunique
	'''
	hashDict = {}
	for astrRow in mat:
		astrNames, strVal = astrRow[:-1], astrRow[-1]
		#populate a dictionary with the set of names as key and the numerical value as its value  
		hashDict[frozenset(astrNames)] = strVal 
	#then return a new matrix object 
	return [([i for i in k]+ [hashDict[k]]) for k in hashDict.keys()]

def makeUnique( mat, strSplit ):
	'''
	splits up a///b;
	make sure to run BEFORE handleDoubleEntries
	'''
	outmat = [] 
	for astrRow in mat:
		astrNames, strVal = astrRow[:-1], astrRow[-1]
		if strVal and any(map(lambda x: x.find(strSplit),astrNames)):
			astrSplit = map(lambda x: x.split(strSplit),astrNames)
			outmat += map(lambda v: list(v) + [strVal],[x for x in itertools.product(*astrSplit)]) 	
		else:
			outmat.append(astrRow)		
	return outmat 

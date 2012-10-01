#!/usr/bin/env python
'''
make gene mapping unique 
for NxM mappings and handle duplicate entries
'''
import sets
import itertools 
import sys 
import csv 
import os

if len(sys.argv[1:]) < 2:
	raise Exception("Usage: makeunique.py inputfile.dat outputfile.dat")

c_strInput, c_strOutput				= sys.argv[1:3] 
c_strRowSplit		 			= sys.argv[3] if len(sys.argv[1:]) > 2 else "2"
c_strSplit					= sys.argv[4] if len(sys.argv[1:]) > 3 else "///"
c_iHeaderSkip                                   = 2 if os.path.splitext(os.path.basename(c_strInput))[1] == ".pcl" else 0

aastrHeaders, aastrMatIn 			= ([x for x in csv.reader(open(c_strInput),csv.excel_tab)])[:c_iHeaderSkip], \
							([x for x in csv.reader(open(c_strInput),csv.excel_tab)])[c_iHeaderSkip:]

def handleDoubleEntries( mat ):
	'''
	gets rid of double entries isomorphic up to permutation;
	make sure to run AFTER makeunique
	'''
	nameSet = set([])
	outmat = [] 
	for astrRow in mat:
		astrNames, astrVals = astrRow[:int(c_strRowSplit)], astrRow[int(c_strRowSplit):]
		lenNames = len(astrNames)
		if (len(frozenset(astrNames)) == lenNames and not(frozenset(astrNames) in nameSet)):
			nameSet |= set([frozenset(astrNames)])
			outmat.append(astrRow)
	return outmat

def makeUnique( mat, strSplit ):
	'''
	splits up a///b;
	make sure to run BEFORE handleDoubleEntries
	'''
	outmat = [] 
	for astrRow in mat:
		astrNames, astrVals = astrRow[:int(c_strRowSplit)], astrRow[int(c_strRowSplit):]
		if any(astrVals) and reduce(lambda y,z: y or z, map(lambda x: x.find(strSplit)!=-1,astrNames)):
			astrSplit = map(lambda x: x.split(strSplit),astrNames)
			outmat += map(lambda v: list(v) + astrVals,[x for x in itertools.product(*astrSplit)]) 	
		else:
			outmat.append(astrRow)		
	return outmat
		
#Execute
csvw = csv.writer(open(c_strOutput,"w"), csv.excel_tab) 
for row in aastrHeaders + handleDoubleEntries(makeUnique(aastrMatIn,c_strSplit)):
	csvw.writerow( row )

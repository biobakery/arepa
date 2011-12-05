import arepa
import os
import sys
import csv 
import subprocess

manual_sample_keys = ['sample_name', 'sample_type', 'subtype', 'primarysite', 'arrayedsite', 'summarygrade', 'summarystage', 'T', 'substage', 'G', 'N', 'M']

def grab_sample_curated_data( c_strID, dummylist = None, dummydict = None ):
	if not dummydict:
		dummydict = {}
	dictR = csv.DictReader(open( c_strID + '_curated_pdata.txt', 'rb'), delimiter='\t')
	def adder( dictR, key, dummylist = None ):
		if not dummylist:
			dummylist = []
		for item in dictR:
			dummylist.append(item[key])
		return dummylist
	for key in manual_sample_keys:
		dictR = csv.DictReader(open( c_strID + '_curated_pdata.txt', 'rb'), delimiter='\t')
		dummydict[key] = adder( dictR, key )
	return dummydict 

	
			


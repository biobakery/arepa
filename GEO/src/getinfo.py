#!/usr/bin/env python 
'''
acquire intermediate information about dataset, 
used to get around pathologies in scons build
'''

import arepa 
import sys 
import re 

pHashRE = {"gse": r'Series_platform_taxid\t"([0-9]*)"', "gds": r'dataset_sample_organism = ([A-Za-z0-9_\- ]*)'}

strf = sys.stdin.read() 

for strKey,strVal in pHashRE.items():
	astrMatch = re.findall( strVal, strf )
	if astrMatch:
		if strKey == "gse":
			print astrMatch[0]
		elif strKey == "gds":
			print arepa.org2taxid( astrMatch[0] )

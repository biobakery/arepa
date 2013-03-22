#!/usr/bin/env python
'''
Parses gpl table from GEO website 
and outputs possible gene table 

Usage: gpl2txt.py [hmtl|url] <fileout.map> 
'''

import sys 
import csv 
import re 
from cStringIO import StringIO
from urllib2 import urlopen

c_strREmatch		= r'<pre>(.*)<br>.*</pre>'
c_strHeadermatch	= r'<strong>([\w ]+)</strong>'		
c_strHypermatch		= r'>(\w+)</'

pHash				= { "ID": "Affy", "ORF": "HGNC" }

def _getName( strLine ):
	if strLine.find("<") == -1:
		return strLine 
	else:
		astrFind = re.findall( c_strHypermatch, strLine ) 
		return astrFind[0] if astrFind else " "

strInFile	= sys.argv[1]
strOutFile	= sys.argv[2] if (sys.argv[1:] > 1) else None 

if ("http" in strInFile) or ("ftp" in strInFile):
	urlr = urlopen( strInFile )
	strInput = urlr.read().strip()
else:
	f = open( strInFile )
	strInput = f.read().strip()

astrMatch = re.findall( c_strREmatch, strInput, re.S )
strMatch = astrMatch[0] if astrMatch else None 

if strMatch:
	csvr = csv.reader( StringIO(strMatch) , csv.excel_tab)
	astrOut = []
	astrHeaders = None 
	for line in csvr:
		if (not line) or any([col.startswith("#") for col in line]): 
			continue	
		elif not(astrHeaders):
			astrHeaders = map( lambda s: s.strip() ,re.findall( c_strHeadermatch, "".join(line) ))
			astrHeadersMapped = [pHash.get(s) or s for s in astrHeaders]
			astrOut.append( astrHeadersMapped )
		else:
			astrTmp = [_getName(s) for s in line]
			astrOut.append( astrTmp )
			
	if astrOut:
		with (open( strOutFile, "w" ) if strOutFile else sys.stdout) as outputf:
			for strOut in astrOut:
				outputf.write( "\t".join( strOut ) + "\n" )
	else:
		with (open( strOutFile, "w" ) if strOutFile else sys.stdout) as outputf:
			outputf.write("\n")

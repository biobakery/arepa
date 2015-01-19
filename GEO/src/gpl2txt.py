#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

gpl2txt.py:

Parses gpl table from GEO website 
and outputs possible gene table 

Usage: gpl2txt.py [hmtl|url] <fileout.map> 
"""

import sys 
import csv 
import re 
from io import StringIO
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
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
	csvr = csv.reader( StringIO(strMatch), csv.excel_tab)
	astrOut = []
	astrHeaders = None 
	for line in csvr:
		if (not line) or any([col.startswith("#") for col in line]): 
			continue	
		elif not(astrHeaders):
			astrHeaders = [s.strip() for s in re.findall( c_strHeadermatch, "".join(line) )]
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

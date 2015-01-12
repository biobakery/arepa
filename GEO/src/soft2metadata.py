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
"""

import sfle
import arepa
import gzip
import metadata
import re
import soft
import sys
import csv
import hashlib

strStatus 	= sys.argv[1]
strMetadata = sys.argv[2] or None 
astrGPLGZs	= sys.argv[3:]

c_hashkeyCurated		= "curated"

def metadatum( funcMetadata, strValue ):
	hashOut.setdefault( strID, set() ).add( strValue )

pSOFT = soft.CSOFT( )
for strGPLGZ in astrGPLGZs:
	pSOFT.open( gzip.open( strGPLGZ ) )
pSOFT.open( sys.stdin )

pMetadata = metadata.open( )
for pDS in list(pSOFT.get( "DATASET" ).values( )):
	pMetadata.pmid( pDS.get_attribute( "dataset_pubmed_id" ) )
	pMetadata.title( pDS.get_attribute( "dataset_title" ) )
	pMetadata.gloss( pDS.get_attribute( "dataset_description" ) )
	pMetadata.type( re.sub( r' by .+$', "", ( pDS.get_attribute( "dataset_type" ) or "" ).lower( ) ) )
	pMetadata.channels( pDS.get_attribute( "dataset_channel_count" ) )
	pMetadata.conditions( pDS.get_attribute( "dataset_sample_count" ) )
	pMetadata.platform( pDS.get_attribute( "dataset_platform" ) )
	pMetadata.taxid( arepa.org2taxid( pDS.get_attribute( "dataset_sample_organism" ) ) )
	#pMetadata.checksum(hashlib.md5(open(pDS, 'rb').read()).hexdigest())
	pMetadata.checksum(hashlib.md5.new(pDS.get_attribute( "dataset" )).digest())
	# pMetadata.checksum(md5.new(pSOFT.open( gzip.open( strGPLGZ ) )).digest())

# Auxillary Metadata 
if strMetadata:
	astrHeaders = None
	for astrLine in csv.reader( open( strMetadata ), csv.excel_tab ):
		if astrHeaders:
			for i in range( len( astrLine ) ):
				pMetadata.setdefault( astrHeaders[i], [] ).append( astrLine[i] )
		else:
			pMetadata[c_hashkeyCurated] = astrLine 
			astrHeaders = astrLine

# Add Mapping Status and Save
k, v = sfle.readcomment( open( strStatus ) )[0].split("\t")
pMetadata.update({k:v})
pMetadata.save( sys.stdout )

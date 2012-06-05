#!/usr/bin/env python 

import arepa 
import csv
import metadata
import re
import sys

c_strID 		= arepa.cwd( ) 
c_fileRMetadataTXT 	= c_strID + "_rmetadata.txt"

c_hashSingleKeys	= {
	"Series_sample_taxid"		: "taxid",
	"Series_type"			: "type",
	"Series_platform_id"		: "platform",
	"Series_title"			: "title",
	"Series_summary"		: "gloss",
	"Series_pubmed_id"		: "pmid" 
}

c_hashMultipleKeys	= {
	"Sample_channel_count"	: "channels",
}

c_hashkeyCondition		= "conditions"
c_hashkeyCurated		= "curated"

def _stripquotes( strIn ):
	mtch = re.search( r'^"(.*)"$', strIn )
	if mtch:
		strIn = mtch.group( 1 )
	return strIn

if len( sys.argv ) < 2:
	raise Exception( "Usage: series2metadata.py <id> [curated.txt] < <series.txt>" )
strID = sys.argv[1]
strMetadata = sys.argv[2] if ( len( sys.argv ) > 2 ) else None

pMetadata = metadata.open( )

for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
	if not ( astrLine and astrLine[0] and ( astrLine[0][0] == "!" ) ):
		continue
	strFrom = astrLine[0][1:]
	
	strTo = c_hashSingleKeys.get( strFrom )
	if strTo:
		strPrev = pMetadata.get( strTo, "" )
		if strPrev:
			strPrev += "\n"
		strPrev += _stripquotes( astrLine[1] )
		pMetadata[strTo] = strPrev
		continue
	
	strTo = c_hashMultipleKeys.get( strFrom )
	if strTo:
		astrCur = [_stripquotes( s ) for s in astrLine[1:]]
		pMetadata[strTo] = astrCur
		if not pMetadata[c_hashkeyCondition]:
			pMetadata[c_hashkeyCondition] = len( astrCur ) 

#BUGBUG: This does not correctly handle condition # matching or non-curated default values
#if curated metadata does not exist, then use R-generated metadata. 

if strMetadata:
	astrHeaders = None
	for astrLine in csv.reader( open( strMetadata ), csv.excel_tab ):
		if astrHeaders:
			for i in range( len( astrLine ) ):
				pMetadata.setdefault( astrHeaders[i], [] ).append( astrLine[i] )
		else:
			pMetadata[c_hashkeyCurated] = astrLine 
			astrHeaders = astrLine
else:
	astrHeaders = None 
	for astrLine in csv.reader( open( c_fileRMetadataTXT ) ):
		if astrHeaders:
			for i in range( len( astrLine )):
				pMetadata[astrHeaders[i]].append( astrLine[i] )
				
		else:
			pMetadata[c_hashkeyCurated] = astrLine 
			astrHeaders = astrLine
			for item in astrHeaders:
				pMetadata.set( item, [] ) 

pMetadata.save( )

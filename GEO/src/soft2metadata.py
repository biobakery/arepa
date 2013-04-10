#!/usr/bin/env python

import sfle
import arepa
import gzip
import metadata
import re
import soft
import sys
import csv

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
for pDS in pSOFT.get( "DATASET" ).values( ):
	pMetadata.pmid( pDS.get_attribute( "dataset_pubmed_id" ) )
	pMetadata.title( pDS.get_attribute( "dataset_title" ) )
	pMetadata.gloss( pDS.get_attribute( "dataset_description" ) )
	pMetadata.type( re.sub( r' by .+$', "", ( pDS.get_attribute( "dataset_type" ) or "" ).lower( ) ) )
	pMetadata.channels( pDS.get_attribute( "dataset_channel_count" ) )
	pMetadata.conditions( pDS.get_attribute( "dataset_sample_count" ) )
	pMetadata.platform( pDS.get_attribute( "dataset_platform" ) )
	pMetadata.taxid( arepa.org2taxid( pDS.get_attribute( "dataset_sample_organism" ) ) )

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
k,v = sfle.readcomment( open( strStatus ) )[0].split("\t")
pMetadata.update({k:v})
pMetadata.save( sys.stdout )

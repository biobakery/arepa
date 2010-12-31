#!/usr/bin/env python

import arepa
import gzip
import re
import soft
import sys

def enhash( hashOut, strID, strValue ):

	if strValue:
		hashOut.setdefault( strID, set() ).add( strValue )

astrGPLGZs = sys.argv[1:]

pSOFT = soft.CSOFT( )
for strGPLGZ in astrGPLGZs:
	pSOFT.open( gzip.open( strGPLGZ ) )
pSOFT.open( sys.stdin )

hashValues = {}
for pDS in pSOFT.get( "DATASET" ).values( ):
	enhash( hashValues, "pmids", pDS.get_attribute( "dataset_pubmed_id" ) )
	enhash( hashValues, "title", pDS.get_attribute( "dataset_title" ) )
	enhash( hashValues, "gloss", pDS.get_attribute( "dataset_description" ) )
	enhash( hashValues, "types", re.sub( r' by .+$', "", ( pDS.get_attribute( "dataset_type" ) or "" ).lower( ) ) )
	enhash( hashValues, "channels", pDS.get_attribute( "dataset_channel_count" ) )
	enhash( hashValues, "conditions", pDS.get_attribute( "dataset_sample_count" ) )
	enhash( hashValues, "platform", pDS.get_attribute( "dataset_platform" ) )
	enhash( hashValues, "taxids", arepa.org2taxid( pDS.get_attribute( "dataset_sample_organism" ) ) )
for strKey, setValues in hashValues.items( ):
	print( "\t".join( (strKey, "|".join( filter( lambda s: s, setValues ) )) ) )

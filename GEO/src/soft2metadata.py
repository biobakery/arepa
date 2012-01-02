#!/usr/bin/env python

import arepa
import gzip
import metadata
import re
import soft
import sys

def metadatum( funcMetadata, strValue ):

		hashOut.setdefault( strID, set() ).add( strValue )

astrGPLGZs = sys.argv[1:]

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
pMetadata.save( sys.stdout )

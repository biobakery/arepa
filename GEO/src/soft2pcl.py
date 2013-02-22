#!/usr/bin/env python
'''Convert soft file to pcl
Usage: soft2pcl.py < [stdin] <input.txt.gz> > <output.pcl>  
'''

import gzip
import soft
import sys
import math 

c_iMaximumValue 	= 50
c_iMaximumCount 	= 50
c_strReplace 		= "NaN" # "NaN" works for both R and python as a "not-a-number" classifier 
c_iSkip			= 2	

## Function Definitions 

def parse( pDS, iSkip = c_iSkip, strReplace = c_strReplace ):
	iCountBig = 0 
	for iRow in range( pDS.rows() ):
		dummyRow = [] 
		for i, strVal in enumerate(pDS.row( iRow )):
			if i < iSkip:
				dummyRow.append(strVal)
				continue 
			else:
				try:
					tmpVal = float(strVal)
				except ValueError:
					tmpVal = strReplace 
				if isinstance( tmpVal, float ):
					if tmpVal > c_iMaximumValue: iCountBig+= 1 
				dummyRow.append(str(tmpVal))
		pDS.set_row( iRow, dummyRow )
	return ( iCountBig >= c_iMaximumCount )

def transform( pDS, iSkip = c_iSkip ):
	'''Criteria for log-transforming data :
	 >= c_iMaximumCount data points with values >= c_dMaximumValue
	'''
	f = lambda x: str(math.log(x,2))
	for iRow in range( pDS.rows( ) ):
		dummyRow = [] 
		astrRowTmp = pDS.row( iRow )
		for strVal in astrRowTmp[iSkip:]:
			try:
				tmpVal = f(float(strVal))
			except ValueError, TypeError:
				tmpVal = strVal 
			dummyRow.append(tmpVal)
		astrRow = astrRowTmp[:iSkip] + dummyRow 
		pDS.set_row( iRow, astrRow )
	return True
 
## Execution 

astrGPLGZs 	= sys.argv[1:]
pSOFT 		= soft.CSOFT( )

for strGPLGZ in astrGPLGZs:
	pSOFT.open( gzip.open( strGPLGZ ) )

pSOFT.open( sys.stdin )

pDS 		= pSOFT.get( "DATASET" ).values( )[0]
apAnnos 	= pSOFT.get( "Annotation" ).values( )
aiAnnos 	= [p.column( "Gene ID" ) for p in apAnnos]
aiColumns 	= filter( lambda i: pDS.column( i )[0].startswith( "GSM" ), range( pDS.columns( ) ) )

print( "GID	NAME	GWEIGHT	" + "\t".join( pDS.column( i )[1] for i in aiColumns ) )
print( "EWEIGHT		" + ( "	1" * len( aiColumns ) ) )

fTransform = parse( pDS )
if fTransform: 
	transform( pDS )

for iRow in range( pDS.rows( ) ):
	astrRow = pDS.row( iRow )
	for strID in astrRow[0].split( "///" ):
		print( "\t".join( [strID, astrRow[1]] + ["1"] + [astrRow[i] for i in aiColumns] ) )


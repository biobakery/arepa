#!/usr/bin/env python

import gzip
import soft
import sys
import math as M

# Criteria for log transforming data :
# >= c_iMaximumCount data points with values >= c_dMaximumValue

c_dMaximumValue = 50
c_iMaximumCount = 50

astrGPLGZs = sys.argv[1:]

pSOFT = soft.CSOFT( )
for strGPLGZ in astrGPLGZs:
	pSOFT.open( gzip.open( strGPLGZ ) )
pSOFT.open( sys.stdin )

pDS = pSOFT.get( "DATASET" ).values( )[0]
apAnnos = pSOFT.get( "Annotation" ).values( )
aiAnnos = [p.column( "Gene ID" ) for p in apAnnos]
aiColumns = filter( lambda i: pDS.column( i )[0].startswith( "GSM" ), range( pDS.columns( ) ) )
print( "GID	NAME	GWEIGHT	" + "\t".join( pDS.column( i )[1] for i in aiColumns ) )
print( "EWEIGHT		" + ( "	1" * len( aiColumns ) ) )

#### Note: "NaN" works for both R and python as a "not-a-number" classifier 
def noNull():
	def mapNull( str ):
		if str == "null":
			return "NaN"
		else:
			return str 
	for iRow in range( pDS.rows() ):
		astrRow = pDS.row( iRow )
		astrRow[2:] = map(mapNull, astrRow[2:]) 

def countBig():
	n = 0 
	for iRow in range( pDS.rows( ) ):
		if n >= c_iMaximumCount:
			return True	
		else: 
			astrRow = pDS.row( iRow ) 
			for expr in astrRow[2:]: 
				if float(expr) >= c_dMaximumValue:
					n+=1 
				else:
					continue    
	return False 

def transform():
	l2 =  lambda x: M.log(x,2) 
	if countBig():
		for iRow in range( pDS.rows( ) ):
			astrRow = pDS.row( iRow )
			astrRow[2:] = map(str,map(l2,map(float, astrRow[2:]))) 

def printTable():
	noNull()
	transform()
	for iRow in range( pDS.rows( ) ):
        	astrRow = pDS.row( iRow )              
        	for strID in astrRow[0].split( "///" ):
                	print( "\t".join( [strID, astrRow[1]] + ["1"] + [astrRow[i] for i in aiColumns] ) )

#Execute 
printTable()  

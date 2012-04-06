#!/usr/bin/env python

import gzip
import soft
import sys
import math as M

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

#I need to determine if I want to log transform or not
#criteria: > 50 with expression > 50 

def countBig():
	n = 0 
	for iRow in range( pDS.rows( ) ):
		if n >= 50:
			return True	
		else: 
			astrRow = pDS.row( iRow ) 
			for expr in astrRow[2:]: 
				if expr < 50:
					continue 
				else:
					n+=1   
	return False 

def transform():
	l2 = lambda x: M.log(x,2) 
	if countBig():
		for iRow in range( pDS.rows( ) ):
			astrRow = pDS.row( iRow )
			astrRow[2:] = map(str,map(l2,map(float, astrRow[2:]))) 
	return None

def printTable():
	transform()
	for iRow in range( pDS.rows( ) ):
        	astrRow = pDS.row( iRow )
        	#This annotation stuff is junk 
        	#for iAnno in range( len( apAnnos ) ):
        	#       if aiAnnos[iAnno] == None:
        	#               continue
        	#       pAnno = apAnnos[iAnno]
        	#       iRow = pAnno.row( astrRow[0] )
                	#strAnno = None if ( iRow == None ) else pAnno.get( iRow, aiAnnos[iAnno] ) 
                	#if strAnno:
                	#       astrRow[1] = "|".join( astrRow[0:2] )
        	       	#       astrRow[0] = strAnno
               
        	for strID in astrRow[0].split( "///" ):
                	print( "\t".join( [strID, astrRow[1]] + ["1"] + [astrRow[i] for i in aiColumns] ) )

#Execute 
printTable()  

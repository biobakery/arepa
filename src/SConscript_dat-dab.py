#!/usr/bin/env python 

'''
shared code across modules 
handles all behavior pertaining to 
mapping dat to dab and generating quant files 
'''

def funcDAB( pE, fileOutDAB, afileInDAT ):
	def _funcDAB( target, source, env ):
		strT, astrSs = sfle.ts( target, source )
		strOut, strMap = astrSs[:2]
		return sfle.ex( ("Dat2Dab", "-o", strT, "-i", ( strOut if sfle.isempty( strMap ) else strMap )) )

	return pE.Command( fileOutDAB, afileInDAT, _funcDAB)

def funcQUANT( pE, fileQUANTin ):
	
	return sfle.scmd( pE, "echo '0.5\t1.5'", fileQUANTin ) 	

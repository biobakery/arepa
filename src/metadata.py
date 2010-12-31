#!/usr/bin/env python

import sys

class CMetadata:
	
	def __init__( self ):
		
		self._clear( )
	
	def _clear( self ):
		
		self.m_hashData = {}
	
	def _accessor( self, strKey, strValue ):

		if strValue:
			self.m_hashData.setdefault( strKey, set() ).add( strValue )
		else:
			return self.m_hashData.get( strKey )
		
	def open( self, fileIn ):
		
		self._clear( )
		for strLine in fileIn:
			astrLine = strLine.strip( ).split( "\t" )
			if len( astrLine ) != 2:
				continue
			self.m_hashData[astrLine[0]] = set("|".split( astrLine[1] ))
			
	def save( self, fileOut ):
		
		for strKey, setValues in self.m_hashData.items( ):
			fileOut.write( "%s\n" % "\t".join( (strKey, "|".join( filter( lambda s: s, setValues ) )) ) )
for strKey in ["taxid", "type", "pmid", "platform", "title", "gloss", "channels", "conditions"]:
	def funcKey( self, strValue = None, strKey = strKey ):
		return self._accessor( strKey, strValue )
	setattr( CMetadata, strKey, funcKey )

if __name__ == "__main__":
	pTest = CMetadata( )
	sys.stderr.write( "%s\n" % dir( pTest ) )
	pTest.taxid( "one" )
	pTest.taxid( "two" )
	sys.stderr.write( "%s\n" % pTest.taxid( ) )
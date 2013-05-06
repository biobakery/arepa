#!/usr/bin/env python

import collections
import pickle
import sys
import csv

class CMetadata:
	c_astrStandards	= ["curated", "taxid", "type", "pmid", "platform", "title", "gloss", "channels", "conditions", "mode", "technique"]
	c_fCollapse		= True
	
	def __init__( self ):
		
		self.m_hashData = {}
	
	def _accessor( self, strKey, strValue = None ):
		
		if strValue == None:
			return self.get( strKey )
		self[strKey] = strValue
	
	def __getitem__( self, strKey ):
		
		return self.get( strKey )
	
	def __setitem__( self, strKey, pValue ):
		
		self.set( strKey, pValue )

	def keys(self):
		return self.m_hashData.keys()
	
	def remove( self, strKey ):
		return self.m_hashData.pop( strKey )  
		
	def get( self, strKey, pValue = None ):
		
		return self.m_hashData.get( strKey, pValue )
	
	def set( self, strKey, pValue, fCollapse = c_fCollapse ):

		if fCollapse and isinstance( pValue, collections.Iterable ) and \
			( len( pValue ) == 1 ):
			pValue = list(pValue)[0]
		self.m_hashData[strKey] = pValue
		
	def setdefault( self, strKey, pValue, fCollapse = c_fCollapse ):
		
		pRet = self.get( strKey )
		if pRet:
			return pRet
		self.set( strKey, pValue, fCollapse )
		return pValue
	
	def update( self, hashData, fCollapse = c_fCollapse ):
		
		for strKey, pValue in hashData.items( ):
			self.set( strKey, pValue, fCollapse )
		
	def open( self, fileIn ):
		
		self.m_hashData = pickle.load( fileIn )
			
	def save( self, fileOut = sys.stdout ):

		pickle.dump( self.m_hashData, fileOut, -1 )
		
	def save_text( self, fileOut = sys.stdout ):

		csvw = csv.writer( fileOut, csv.excel_tab )
		for strKey, pValue in self.m_hashData.items( ):
			csvw.writerow( (strKey, "%s" % pValue) )

for strKey in CMetadata.c_astrStandards:
	def funcKey( self, strValue = None, strKey = strKey ):
		return self._accessor( strKey, strValue )
	setattr( CMetadata, strKey, funcKey )

def open( fileIn = None ):
	
	pRet = CMetadata( )
	if fileIn:
		pRet.open( fileIn )
	return pRet

if __name__ == "__main__":
	pTest = open( )
	sys.stderr.write( "%s\n" % dir( pTest ) )
	pTest.taxid( "one" )
	pTest.taxid( "two" )
	sys.stderr.write( "%s\n" % pTest.taxid( ) )

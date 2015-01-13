#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import collections
import pickle
import sys
import csv
import gzip

class CMetadata:
	c_astrStandards	= ["curated", "taxid", "type", "pmid", "platform", "title", "gloss", "channels", "conditions", "mode", "technique", "checksum"]
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
		return list(self.m_hashData.keys())
	
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
		
		for strKey, pValue in list(hashData.items( )):
			self.set( strKey, pValue, fCollapse )
		
	def open( self, fileIn ):
		
		self.m_hashData = pickle.load( fileIn )
			
	def save( self, fileOut = sys.stdout ):

		pickle.dump( self.m_hashData, fileOut, -1 )
		
	def save_text( self, fileOut = sys.stdout ):

		csvw = csv.writer( fileOut, csv.excel_tab )
		for strKey, pValue in list(self.m_hashData.items( )):
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
def get_md5sum(file, gzipped=None):
    """ Get the md5sum of a file
    """
    
    block_size=128
    md5=hashlib.md5()
    md5sum=""
    try:
        if gzipped:
            file_handle=gzip.open(file)
        else:
            file_handle=open(file)
        data=file_handle.read(block_size)
        while data:
            md5.update(data.encode('utf-8'))
            data=file_handle.read(block_size)
        md5sum=md5.hexdigest()
        file_handle.close()
    except (EnvironmentError,UnicodeDecodeError):
        md5sum=""

    return md5sum
            
if __name__ == "__main__":
	pTest = open( )
	sys.stderr.write( "%s\n" % dir( pTest ) )
	pTest.taxid( "one" )
	pTest.taxid( "two" )
	sys.stderr.write( "%s\n" % pTest.taxid( ) )

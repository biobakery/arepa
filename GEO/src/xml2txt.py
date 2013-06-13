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

import arepa
import csv
import sys
import xml.sax

class CParser(xml.sax.handler.ContentHandler):
	
	def __init__( self, strType, setstrTaxa ):
		
		self.m_strTag = self.m_strID = self.m_strTaxon = None
		self.m_strType = strType
		self.m_setstrTaxa = setstrTaxa

	def _clean( self, strToken ):
		
		if ( ( self.m_strType == "GSE" ) and ( strToken.find( "2" ) == 0 ) ) or \
			( ( self.m_strType == "GPL" ) and ( strToken.find( "1" ) == 0 ) ):
			strToken = str(int(strToken[1:]))
		return strToken.strip( )

	def startElement( self, strName, hashAttrs ):

		self.m_strTag = strName
		if strName == "Id":
			self.m_strID = self.m_strTaxon = ""
		elif strName == "Item":
			self.m_strName = hashAttrs.get( "Name" )
		
	def endElement( self, strName ):
		
		if ( strName == "DocSum" ) and self.m_strID and \
			( ( not self.m_setstrTaxa ) or ( self.m_strTaxon.strip( ) in self.m_setstrTaxa ) ):
			print( self.m_strType + self._clean( self.m_strID ) )
		
	def characters( self, strText ):

		if self.m_strTag == "Id":
			self.m_strID += strText
		elif ( self.m_strTag == "Item" ) and ( self.m_strName == "taxon" ):
			self.m_strTaxon += strText

if len( sys.argv ) < 2:
	raise Exception( "Usage: xml2txt.py <type> [taxids.txt] < <data.xml>" )
strType = sys.argv[1].upper( )
strTaxa = sys.argv[2] if ( len( sys.argv ) > 2 ) else None

setstrTaxa = set()
if strTaxa:
	for astrLine in csv.reader( open( strTaxa ), csv.excel_tab ):
		setstrTaxa.add( astrLine[1] )

pSAX = xml.sax.make_parser( )
pSAX.setContentHandler( CParser( strType, setstrTaxa ) )
pSAX.parse( sys.stdin )
sys.stdout.write(" ")

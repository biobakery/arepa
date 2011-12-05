#!/usr/bin/env python

import arepa
import sys
import xml.sax

class CParser(xml.sax.handler.ContentHandler):
	
	def __init__( self, strType ):
		
		self.m_strTag = self.m_strID = None
		self.m_strType = strType

	def _clean( self, strToken ):
		
		if ( self.m_strType == "GSE" ) and ( strToken.find( "2" ) == 0 ):
			strToken = str(int(strToken[1:]))
		if ( self.m_strType == "GPL" ) and ( strToken.find( "1" ) == 0 ):
			strToken = str(int(strToken[1:]))
		return strToken

	def startElement( self, strName, hashAttrs ):

		self.m_strTag = strName
		if strName == "Id":
			self.m_strID = ""
		
	def endElement( self, strName ):
		
		if ( strName == "Id" ) and self.m_strID:
			print( self.m_strType + self._clean( self.m_strID ) )
		
	def characters( self, strText ):

		if self.m_strTag == "Id":
			self.m_strID += strText

if len( sys.argv ) != 2:
	raise Exception( "Usage: xml2txt.py <type> < <data.xml>" )
strType = sys.argv[1]

pSAX = xml.sax.make_parser( )
pSAX.setContentHandler( CParser( strType ) )
pSAX.parse( sys.stdin )

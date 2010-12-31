#!/usr/bin/env python

import arepa
import sys
import xml.sax

class CParser(xml.sax.handler.ContentHandler):
	
	def __init__( self ):
		
		self.m_strTag = self.m_strID = None

	def startElement( self, strName, hashAttrs ):

		self.m_strTag = strName
		if strName == "Id":
			self.m_strID = ""
		
	def endElement( self, strName ):
		
		if ( strName == "Id" ) and self.m_strID:
			print( "GDS" + self.m_strID )
		
	def characters( self, strText ):

		if self.m_strTag == "Id":
			self.m_strID += strText

pSAX = xml.sax.make_parser( )
pSAX.setContentHandler( CParser( ) )
pSAX.parse( sys.stdin )

#!/usr/bin/env python

import arepa
import sys
import xml.sax

class CParser(xml.sax.handler.ContentHandler):
	
	def __init__( self, setTaxa ):
		
		self.m_strTag = self.m_strAccession = self.m_strSpecies = None
		self.m_setIDs = set()
		self.m_setTaxa = setTaxa

	def startElement( self, strName, hashAttrs ):

		self.m_strTag = strName
		if strName == "experiment":
			self.m_strAccession = self.m_strSpecies = None
		
	def endElement( self, strName ):
		
		if ( strName == "experiment" ) and self.m_strAccession and self.m_strSpecies and \
			( ( not self.m_setTaxa ) or ( self.m_strSpecies in self.m_setTaxa ) ):
			self.m_setIDs.add( (self.m_strAccession, self.m_strSpecies) )
		
	def characters( self, strText ):

		if self.m_strTag == "accession":
			if not self.m_strAccession:
				self.m_strAccession = strText
		elif self.m_strTag == "species":
			if not self.m_strSpecies:
				self.m_strSpecies = strText
		
	def endDocument( self ):

		print(( "\n".join( "\t".join( astrCur ) for astrCur in self.m_setIDs ) ))

strTaxa = None if ( len( sys.argv ) <= 1 ) else sys.argv[1]

setTaxa = arepa.taxa( strTaxa, True )

pSAX = xml.sax.make_parser( )
pSAX.setContentHandler( CParser( setTaxa ) )
pSAX.parse( sys.stdin )

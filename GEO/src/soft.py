#!/usr/bin/env python

import sys
import re

class CSOFT:
	class CEntity:
		
		def __init__( self, strType, strID ):
			
			self.m_strType = strType
			self.m_strID = strID
			self.m_hashAttrs = {}
			self.m_hashColValues = {}
			self.m_aastrRows = []
			self.m_astrColumns = []
			self.m_hashColumns = {}
			self.m_hashRows = {}
			
		def add_attribute( self, strKey, strValue ):
			
			self.m_hashAttrs[strKey] = strValue
			
		def get_attributes( self ):
			
			return self.m_hashAttrs.keys( )
		
		def get_attribute( self, strKey ):
			
			return self.m_hashAttrs.get( strKey )
		
		def columns( self ):
			
			return len( self.m_astrColumns )
		
		def column( self, pColumn ):
			
			if isinstance( pColumn, int ):
				strCol = self.m_astrColumns[pColumn]
				return (strCol, self.m_hashColValues.get( strCol ))
			
			return self.m_hashColumns.get( pColumn )
		
		def rows( self ):
			
			return len( self.m_aastrRows )
		
		def row( self, pRow ):
			
			if isinstance( pRow, int ):
				return ( self.m_aastrRows[pRow] if ( pRow < len( self.m_aastrRows ) ) else None )
			
			return self.m_hashRows.get( pRow )
		
		def add_row( self, astrRow ):
			
			if self.m_astrColumns:
				self.m_hashRows[astrRow[0]] = len( self.m_aastrRows )
				self.m_aastrRows.append( astrRow )
			else:
				self.m_astrColumns = astrRow
				for i in range( len( astrRow ) ):
					self.m_hashColumns[astrRow[i]] = i
				
		def add_column( self, strKey, strValue ):
			
			self.m_hashColValues[strKey] = strValue
		
		def get( self, iRow, iColumn ):

			astrRow = self.row( iRow )
			return ( astrRow[iColumn] if ( iColumn < len( astrRow or [] ) ) else None )

	def __init__( self ):
		
		self.m_hashhashEntities = {}

	def open( self, fileIn ):
		def funcSplit( strLine ):
			
			strLine = strLine.strip( )
			mtch = re.search( r'^(\S+)\s*=\s*(.+)$', strLine )
			return ( mtch.groups( ) if mtch else (strLine, "") )

		pEntity = None
		for strLine in fileIn:
			strLine = strLine.strip( )
			if strLine[0] == "^":
				strKey, strValue = funcSplit( strLine[1:] )
				pEntity = self.m_hashhashEntities.setdefault( strKey, {} ).setdefault(
					strValue, CSOFT.CEntity( strKey, strValue ) )
			elif strLine[0] == "!":
				strKey, strValue = funcSplit( strLine[1:] )
				pEntity.add_attribute( strKey, strValue )
			elif strLine[0] == "#":
				strKey, strValue = funcSplit( strLine[1:] )
				pEntity.add_column( strKey, strValue )
			else:
				pEntity.add_row( strLine.split( "\t" ) )

	def get( self, strType ):
		
		return self.m_hashhashEntities.get( strType, {} )

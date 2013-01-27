#!/usr/bin/env python
#######################################################################################
# This file is provided under the Creative Commons Attribution 3.0 license.
#
# You are free to share, copy, distribute, transmit, or adapt this work
# PROVIDED THAT you attribute the work to the authors listed below.
# For more information, please see the following web page:
# http://creativecommons.org/licenses/by/3.0/
#
# This file is a component of the SflE Scientific workFLow Environment for reproducible 
# research, authored by the Huttenhower lab at the Harvard School of Public Health
# (contact Curtis Huttenhower, chuttenh@hsph.harvard.edu).
#
# If you use this environment, the included scripts, or any related code in your work,
# please let us know, sign up for the SflE user's group (sfle-users@googlegroups.com),
# pass along any issues or feedback, and we'll let you know as soon as a formal citation
# is available.
#######################################################################################

"""
Examples
~~~~~~~~

``data1.pcl``::

	tid	exp1	exp2
	gene1	1	2
	gene2	3	4
	gene3	5	6

``data2.pcl``::

	tid	exp2	exp3
	gene1	0.1	0.2
	gene3	0.3	0.4
	gene5	0.5	0.6

``Examples``::

	$ merge_tables.py data1.pcl data2.pcl
	tid	exp1	exp2	exp2	exp3
	gene1	1	2	0.1	0.2
	gene2	3	4		
	gene3	5	6	0.3	0.4
	gene5			0.5	0.6

	$ merge_tables.py data2.pcl data1.pcl
	tid	exp2	exp3	exp1	exp2
	gene1	0.1	0.2	1	2
	gene2			3	4
	gene3	0.3	0.4	5	6
	gene5	0.5	0.6		

	$ merge_tables.py -l data1.pcl data2.pcl
	tid	data1: exp1	data1: exp2	data2: exp2	data2: exp3
	gene1	1	2	0.1	0.2
	gene2	3	4		
	gene3	5	6	0.3	0.4
	gene5			0.5	0.6

.. testsetup::

	from merge_tables import *
"""

import argparse
import csv
import os
import re
import sys

def merge( aaastrIn, astrLabels, fLabel, iCol, fRows, fHeaders, ostm ):
	"""
	Outputs the table join of the given pre-split string collection.
	
	:param	aaastrIn:	One or more split lines from which data are read.
	:type	aaastrIn:	collection of collections of string collections
	:param	astrLabels:	Labels (typically file names) of input data.
	:type	astrLabels:	collection of strings
	:param	fInvert:	If true, prepend table name to header row.
	:type	fInvert:	bool
	:param	iCol:		Data column in which IDs are matched (zero-indexed).
	:type	iCol:		int
	:param	fRows:		If true, match IDs on rows rather than columns.
	:type	fRows:		bool
	:param	fHeaders:	If true, assume first row is headers (column labels).
	:type	fHeaders:	bool
	:param	ostm:		Output stream to which matched rows are written.
	:type	ostm:		output stream
	
	>>> astrLabels = ["data1.pcl", "data2.pcl"]
	>>> aastrOne = [s.split( " " ) for s in ("tid exp1 exp2", "gene1 1 2", "gene2 3 4", "gene3 5 6")]
	>>> aastrTwo = [s.split( " " ) for s in ("tid exp2 exp3", "gene1 0.1 0.2", "gene3 0.3 0.4", "gene5 0.5 0.6")]
	>>> merge( [aastrOne, aastrTwo], astrLabels, False, 0, False, True, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp1	exp2	exp2	exp3
	gene1	1	2	0.1	0.2
	gene2	3	4		
	gene3	5	6	0.3	0.4
	gene5			0.5	0.6

	>>> merge( [aastrTwo, aastrOne], astrLabels, False, 0, False, True, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp2	exp3	exp1	exp2
	gene1	0.1	0.2	1	2
	gene2			3	4
	gene3	0.3	0.4	5	6
	gene5	0.5	0.6		

	>>> merge( [aastrOne, aastrTwo], astrLabels, True, 0, False, True, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	data1: exp1	data1: exp2	data2: exp2	data2: exp3
	gene1	1	2	0.1	0.2
	gene2	3	4		
	gene3	5	6	0.3	0.4
	gene5			0.5	0.6

	>>> merge( [aastrOne, aastrTwo], astrLabels, False, 0, True, True, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp1	exp2	exp3
	gene1	1	2
	gene2	3	4
	gene3	5	6
	gene1		0.1	0.2
	gene3		0.3	0.4
	gene5		0.5	0.6

	>>> merge( [aastrOne, aastrTwo], astrLabels, True, 0, True, True, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp1	exp2	exp3
	data1: gene1	1	2
	data1: gene2	3	4
	data1: gene3	5	6
	data2: gene1		0.1	0.2
	data2: gene3		0.3	0.4
	data2: gene5		0.5	0.6
	"""
	
	setstrIDs = set()
	"""The final set of all IDs in any table."""
	ahashIDs = [{} for i in range( len( aaastrIn ) )]
	"""One hash of IDs to row numbers for each input datum."""
	aaastrData = [[] for i in range( len( aaastrIn ) )]
	"""One data table for each input datum."""
	aastrHeaders = [[] for i in range( len( aaastrIn ) )]
	"""The list of non-ID headers for each input datum."""
	strHeader = None
	"""The ID column header."""
	# For each input datum...
	for iIn in range( len( aaastrIn ) ):
		# Remember its input line list, output line list, and ID mapping
		aastrIn, aastrData, hashIDs = (a[iIn] for a in (aaastrIn, aaastrData, ahashIDs))
		# Start at line -2 so that headers are -1 and data are then 0-indexed
		iLine = -2 if fHeaders else -1
		for astrLine in aastrIn:
			iLine += 1
			# Handle indexing differently for rows versus columns
			if fRows:
				strID, astrData = astrLine[0], astrLine[1:]
				if not fHeaders:
					strID, astrData = str(iLine), astrLine
				if ( iLine + 1 ) == iCol:
					# Remember the first ID header name we see for output
					if not strHeader:
						strHeader = strID
					for i in range( len( astrData ) ):
						hashIDs[astrData[i]] = i
				else:
					# This should only trigger the first time to initialize the data matrix
					while len( aastrData ) < len( astrData ):
						aastrData.append( [] )
					aastrHeaders[iIn].append( strID )
					for i in range( len( astrData ) ):
						aastrData[i].append( astrData[i] )
			else:
				# ID is from requested column, data are everything else
				strID, astrData = astrLine[iCol], ( astrLine[:iCol] + astrLine[( iCol + 1 ):] )
				if iLine >= 0:
					if not aastrHeaders[iIn]:
						aastrHeaders[iIn] = [str(i) for i in range( len( astrData ) )]
					hashIDs[strID] = iLine
					aastrData.append( astrData )
				else:
					# Remember the first ID header name we see for output
					if not strHeader:
						strHeader = strID
					aastrHeaders[iIn] = astrData
		# Batch merge every new ID key set
		setstrIDs.update( hashIDs.keys( ) )
		
	csvw = csv.writer( ostm, csv.excel_tab )
	"""
	The following is Python black magic that I dislike, but it's an extremely
	efficient way to flatten a list.  That is, given a list of lists of strings::
	
		[["a", "b"], ["c"], ["d", "e", "f"]]
		
	it flattens their contents into a single list::
	
		["a", "b", "c", "d", "e", "f"]
		
	To parse it, read it as "the list containing every element in every list in
	``aastrHeaders``."
	"""
	astrHeaders = [s for a in aastrHeaders for s in a]
	# If we're labeling headers, prepend each with ``labelname: ``.
	if fLabel:
		iHeader = 0
		for iIn in range( len( aaastrIn ) ):
			for i in range( len( aastrHeaders[iIn] ) ):
				astrHeaders[iHeader] = ": ".join( (re.sub( r'\.[^.]+$', "", os.path.basename( astrLabels[iIn] ) ),
					astrHeaders[iHeader]) )
				iHeader += 1

	# Handle output differently for rows versus columns
	if fRows:
		astrIDs = sorted( setstrIDs )
		# Keys go in first row rather than each row
		csvw.writerow( [strHeader] + astrIDs )
		iHeader = -1
		for iIn in range( len( aaastrIn ) ):
			aastrData, hashIDs = (a[iIn] for a in (aaastrData, ahashIDs))
			# Look up the column numbers (if any) of all IDs in one shot
			aiIDs = [hashIDs.get( s ) for s in astrIDs]
			for iRow in range( len( aastrHeaders[iIn] ) ):
				iHeader += 1
				csvw.writerow( [astrHeaders[iHeader]] +
					[( None if ( i == None ) else aastrData[i][iRow] ) for i in aiIDs] )
	else:
		csvw.writerow( [strHeader] + astrHeaders )
		for strID in sorted( setstrIDs ):
			astrOut = []
			for iIn in range( len( aaastrIn ) ):
				aastrData, hashIDs = (a[iIn] for a in (aaastrData, ahashIDs))
				# Look up the row number of the current ID in the current dataset, if any
				iID = hashIDs.get( strID )
				# If not, start with no data; if yes, lift out stored data row
				astrData = [] if ( iID == None ) else aastrData[iID]
				# Pad output data to correct length (possibly starting from nothing)
				astrData += [None] * ( len( aastrHeaders[iIn] ) - len( astrData ) )
				astrOut += astrData
			csvw.writerow( [strID] + astrOut )

argp = argparse.ArgumentParser( prog = "merge_tables.py",
	description = """Performs a table join on one or more tab-delimited text files.""" )
argp.add_argument( "aistms",	metavar = "input.pcl",
	type = argparse.FileType( "r" ),	nargs = "+",
	help = "One or more tab-delimited text tables to join" )
argp.add_argument( "-t",		dest = "fTranspose",	action = "store_true",
	help = "If true, join on column rather than row IDs" )
argp.add_argument( "-l",		dest = "fLabel",		action = "store_true",
	help = "If true, prepend table name to column headers to prevent collisions" )
argp.add_argument( "-c",		dest = "iCol",			metavar = "column",
	type = int,		default = 0,
	help = "Column number (zero-indexed) from which table IDs are read" )
argp.add_argument( "-d",		dest = "fHeaders",		action = "store_false",
	help = "If true, assume the first row is data, not headers" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	merge( [csv.reader( f, csv.excel_tab ) for f in args.aistms], [f.name for f in args.aistms],
		args.fLabel, args.iCol, args.fTranspose, args.fHeaders, sys.stdout )

if __name__ == "__main__":
	_main( )

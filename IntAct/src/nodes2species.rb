#!/usr/bin/env ruby

C_astrInclude	= ["Archaea", "Bacteria", "Viruses"]

def output( iID, aaiChildren, aiNames )

	puts( aiNames[ iID ] )
	( aaiChildren[ iID ] || [] ).each do |iChild|
		output( iChild, aaiChildren, aiNames ); end; end

def output2( iID, aaiChildren, aiNames, iDepth )

	puts( ( " " * iDepth ) + aiNames[ iID ] + "\t" + iID.to_s )
	iDepth += 1
	( aaiChildren[ iID ] || [] ).each do |iChild|
		output2( iChild, aaiChildren, aiNames, iDepth ); end; end

if( ARGV.length != 1 )
	raise( "Usage: nodes2species.rb <names.dmp> < <nodes.dmp>" ); end
strNames = ARGV[ 0 ]

aiInclude = []
aiNames = []
IO.foreach( strNames ) do |strLine|
	strID, strName, strBlank, strType = strLine.strip.split( /\s*\|\s*/ )
	if( strType == "scientific name" )
		iID = strID.to_i
		aiNames[ iID ] = strName
		if( C_astrInclude.include?( strName ) )
			aiInclude.push( iID ); end; end; end

aaiChildren = []
STDIN.each do |strLine|
	astrLine = strLine.strip.split( /\s*\|\s*/ )
	iChild, iParent = astrLine[ 0, 2 ].map do |str|
		str.to_i; end
	if( !( aiChildren = aaiChildren[ iParent ] ) )
		aaiChildren[ iParent ] = aiChildren = []; end
	aiChildren.push( iChild ); end

aiInclude.each do |i|
	output2( i, aaiChildren, aiNames, 0 ); end

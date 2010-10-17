#!/usr/bin/env ruby

if( ARGV.length != 1 )
	raise( "Usage: subdirectories.rb <species.txt> < <intact.txt>" ); end
strSpecies = ARGV[0]

hashSpecies = {}
IO.foreach( strSpecies ) do |strLine|
	astrLine = strLine.strip.split( /\t/ )
	if( astrLine[0] =~ /^(\S+)\s+(\S+)/ )
		astrLine[0] = $1 + "_" + $2.sub( /\.$/, "" ); end
	hashSpecies[astrLine[1]] = astrLine[0]; end

STDIN.each do |strLine|
	astrLine = strLine.split( /\t/ ).map do |str|
		str.strip; end
	if( astrLine[0] =~ /^#/ )
		next; end
	strTax1, strTax2 = astrLine[9, 2].map do |str|
		str =~ /taxid:(\d+)/
		$1; end
	if( !strTax1 || ( strTax1 != strTax2 ) )
		strTax1 = "0"; end
	if( !( strTarget = hashSpecies[strTax1] ) )
		next; end
	strDir = "_" + strTarget
	if( !File.exist?( strDir ) )
		system( "mkdir -p " + strDir )
		strTo = strDir + "/Makefile"
		if( !File.exist?( strTo ) )
			system( "cp Makefile.template " + strTo );  end; 
		strTo2 = strDir + "/SConscript"
		if( !File.exist?( strTo2 ) )
			system( "cp SConscript.common " + strTo2);  end; end
	File.open( strDir + "/intact-" + strTarget + ".txt", "a" ) do |fileOut|
		fileOut.puts( strLine ); end; end

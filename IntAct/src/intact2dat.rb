#!/usr/bin/env ruby

C_astrMaps	= Dir.glob( "../maps/*.txt" )
C_astrPres	= %w(Cj Ng Sa Ye Cd Rv Hi Mb Bb CBO Cg Ef FTT FTL HP Nm Pa Vc VCA Ecs Ba BSU)

def make_label( hashhashMap, strToken )

	strOR = C_astrPres.map do |str|
		"(?:" + str + ")"; end.join( "|" )
	if( strToken =~ /^(.*)\s+\([0-9A-Z]+\)$/ )
		strToken = $1; end
	if( strToken =~ /:([^:]+_at)/ )
		strToken = $1; end

	hashTokens = {strToken => true}
	iSize = -1
	while( hashTokens.size != iSize )
		iSize = hashTokens.size
		hashTokens.keys.each do |strCur|
			( hashhashMap[strCur] || {} ).keys.each do |strKey|
				hashTokens[strKey] = true; end; end; end

#	[strToken].concat( ( hashhashMap[strToken] || {} ).keys ).each do |strCur|
	hashTokens.keys.each do |strCur|
		strCur = strCur.strip
		strRet = nil
		case( strCur )
			when /(EF)_(\d+).*at/
				strRet = $1 + $2

			when /(sp[rn]?_\d+)/i
				strRet = $1.upcase

			when /(sp[rn]?)(\d+)(?:#\d+)?$/i
				strRet = $1.upcase + "_" + $2

			when /HPY(\d+)/
				strRet = "HP" + $1

			when /(#{strOR})\S*-(\d+)/
				strRet = ( $1 + $2 ).upcase

			when /((?:#{strOR})\d+)/i
				strRet = $1.upcase

			when /(b\d+)/i
				strRet = $1.upcase; end
		if( strRet && ( strRet.length > 4 ) )
			return strRet; end; end

	return nil; end

hashhashMap = {}
C_astrMaps.each do |strMap|
	aiCols = [0, 1]
	IO.foreach( strMap ) do |strLine|
		astrLine = strLine.chomp.split( /\t/ )
		strFrom, strTo = astrLine[aiCols[0]], astrLine[aiCols[1]]
		if( !( hashTos = hashhashMap[strFrom] ) )
			hashhashMap[strFrom] = hashhashMap[strFrom.upcase] = hashTos = {}; end
		hashTos[strTo] = true; end; end

STDIN.each do |strLine|
	astrLine = strLine.split( /\t/ ).map do |str|
		str.strip; end
	strOnes, strTwos = astrLine[0] + "|" + astrLine[2], astrLine[1] + "|" +
		astrLine[3]
	astrOnes, astrTwos = [strOnes, strTwos].map do |strTokens|
		astrTokens = strTokens.strip.split( /\|/ )
		astrTokens.map do |strToken|
			strToken.split( /:/ )[1] =~ /^([^(]+)/
			$1.upcase; end; end
	strOne = strTwo = nil
	astrOnes.each do |strCur|
		if( strCur = make_label( hashhashMap, strCur ) )
			strOne = strCur
			break; end; end
	astrTwos.each do |strCur|
		if( strCur = make_label( hashhashMap, strCur ) )
			strTwo = strCur
			break; end; end
	if( strOne && strTwo )
		puts( [strOne, strTwo, 1].join( "\t" ) ); end; end

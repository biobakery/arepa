c_fileIDNormPCL		= File( c_strID + "_01norm.pcl" )
c_fileIDPCL			= File( c_strID + ".pcl" )
c_fileIDDAB			= File( c_strID + ".dab" )

#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )
Command( c_fileIDNormPCL, c_fileIDRawPCL, funcIDNormPCL )

#- Impute
def funcIDKNNPCL( target, source, env, iMaxLines = 40000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "KNNImputer < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )
Command( c_fileIDPCL, c_fileIDNormPCL, funcIDKNNPCL )
Default( c_fileIDPCL )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( (sfle.cat( strS ), " | Distancer -o", strT) )
		if ( iLC > 3 ) else arepa.ex( "echo", strT ) )
#Command( c_fileIDDAB, c_fileIDPCL, funcIDDAB )
#Default( c_fileIDDAB )

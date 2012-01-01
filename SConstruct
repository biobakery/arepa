import arepa
import sfle
import sys

c_strURLTaxonomy		= "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"
c_astrExclude			= [
	"ArrayExpress",
	"GEO",
#	"IntAct",
]

c_fileInputTaxa			= File( sfle.d( sfle.c_strDirEtc, "taxa" ) )
c_fileTaxIDs			= File( sfle.d( sfle.c_strDirTmp, "taxids" ) )
c_fileTaxdumpTXT		= File( sfle.d( sfle.c_strDirTmp, "taxdump.txt" ) )
c_fileTaxdumpTARGZ		= File( sfle.d( sfle.c_strDirTmp, "taxdump.tar.gz" ) )
c_fileProgTaxdump2TXT	= File( sfle.d( sfle.c_strDirSrc, "taxdump2txt.py" ) )
c_fileProgTaxdump2Taxa	= File( sfle.d( sfle.c_strDirSrc, "taxdump2taxa.py" ) )

Decider( "MD5-timestamp" )
pE = DefaultEnvironment( )

#===============================================================================
# Shared data setup: NCBI taxonomy
#===============================================================================

sfle.download( pE, c_strURLTaxonomy, c_fileTaxdumpTARGZ )
NoClean( c_fileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strTARGZ = astrSs[:2]
	return sfle.ex( ("tar -xzOf", strTARGZ, "names.dmp nodes.dmp |" , strProg), strT )
Command( c_fileTaxdumpTXT, [c_fileProgTaxdump2TXT, c_fileTaxdumpTARGZ], funcTaxdumpTXT )

afileTaxIDs = sfle.pipe( pE, c_fileTaxdumpTXT, c_fileProgTaxdump2Taxa, c_fileTaxIDs,
	[[True, c_fileInputTaxa]] )

#===============================================================================
# Main SConscript on subdirectories
#===============================================================================

sfle.scons_children( pE, ".", afileTaxIDs, c_astrExclude )

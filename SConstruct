import arepa
import sys

c_fileInputTaxa			= File( arepa.d( arepa.c_strDirEtc, "taxa" ) )
c_fileTaxIDs			= File( arepa.d( arepa.c_strDirTmp, "taxids" ) )
c_fileTaxdumpTXT		= File( arepa.d( arepa.c_strDirTmp, "taxdump.txt" ) )
c_fileTaxdumpTARGZ		= File( arepa.d( arepa.c_strDirTmp, "taxdump.tar.gz" ) )
c_fileProgTaxdump2TXT	= File( arepa.d( arepa.c_strDirSrc, "taxdump2txt.py" ) )
c_fileProgTaxdump2Taxa	= File( arepa.d( arepa.c_strDirSrc, "taxdump2taxa.py" ) )

pE = Environment( )
pE.Dir( arepa.c_strDirTmp )

#===============================================================================
# Shared data setup: NCBI taxonomy
#===============================================================================

arepa.download( pE, "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz", c_fileTaxdumpTARGZ )
pE.NoClean( c_fileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "tar -xzOf " + astrSs[1] + " names.dmp nodes.dmp | " +
		astrSs[0], strT )
pE.Command( c_fileTaxdumpTXT, [c_fileProgTaxdump2TXT, c_fileTaxdumpTARGZ],
	funcTaxdumpTXT )

arepa.pipe( pE, c_fileTaxdumpTXT, c_fileProgTaxdump2Taxa, c_fileTaxIDs,
	[[True, c_fileInputTaxa]] )

#===============================================================================
# Main SConscript on subdirectories
#===============================================================================

arepa.scons_children( pE, globals( ) )

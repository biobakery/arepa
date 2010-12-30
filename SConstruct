import arepa
import sys

pE = Environment( )
c_strInputTaxa			= arepa.d( arepa.c_strDirEtc, "taxa" )
c_strFileTaxIDs			= arepa.d( arepa.c_strDirTmp, "taxids" )
c_strFileTaxdumpTXT		= arepa.d( arepa.c_strDirTmp, "taxdump.txt" )
c_strFileTaxdumpTARGZ	= arepa.d( arepa.c_strDirTmp, "taxdump.tar.gz" )
c_strProgTaxdump2TXT	= arepa.d( arepa.c_strDirSrc, "taxdump2txt.py" )
c_strProgTaxdump2Taxa	= arepa.d( arepa.c_strDirSrc, "taxdump2taxa.py" )

#===============================================================================
# Shared data setup: NCBI taxonomy
#===============================================================================

arepa.download( pE, "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz", c_strFileTaxdumpTARGZ )
NoClean( c_strFileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "tar -xzOf " + astrSs[1] + " names.dmp nodes.dmp | " +
		astrSs[0], strT )
Command( c_strFileTaxdumpTXT, [c_strProgTaxdump2TXT, c_strFileTaxdumpTARGZ],
	funcTaxdumpTXT )

arepa.pipe( pE, c_strFileTaxdumpTXT, c_strProgTaxdump2Taxa, c_strFileTaxIDs,
	[[True, c_strInputTaxa]] )

#===============================================================================
# Main SConscript on subdirectories
#===============================================================================

arepa.scons_children( pE )

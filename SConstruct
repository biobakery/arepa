import sys
try:
	import arepa
except ImportError:
	sys.stderr.write( "********\nNo arepa.py file found - did you remember to run \"export PYTHONPATH=`pwd`/src\"?\n********\n" )
	raise
import sfle

Decider( "MD5-timestamp" )
pE = DefaultEnvironment( )


c_strURLTaxonomy		= "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"
c_astrExclude			= [ "ArrayExpress", "GeneMapper",  
				#,"STRING" 
				#,"GeneMapper", "IntAct", "BioGrid",
				#"Bacteriome", "RegulonDB", "MPIDP" 
					]

c_strURLTaxonomy		= "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz"

c_fileInputTaxa			= sfle.d( pE, sfle.c_strDirEtc, "taxa" ) 
c_fileTaxIDs			= sfle.d( pE, sfle.c_strDirTmp, "taxids" ) 
c_fileTaxdumpTXT		= sfle.d( pE, sfle.c_strDirTmp, "taxdump.txt" ) 
c_fileTaxdumpTARGZ		= sfle.d( pE, sfle.c_strDirTmp, "taxdump.tar.gz" ) 
c_fileProgTaxdump2TXT		= sfle.d( pE, sfle.c_strDirSrc, "taxdump2txt.py" ) 
c_fileProgTaxdump2Taxa		= sfle.d( pE, sfle.c_strDirSrc, "taxdump2taxa.py" )
c_fileInputTaxa			= sfle.d( pE, sfle.c_strDirEtc, "taxa" )
c_fileTaxIDs			= sfle.d( pE, sfle.c_strDirTmp, "taxids" )
c_fileTaxdumpTXT		= sfle.d( pE, sfle.c_strDirTmp, "taxdump.txt" )
c_fileTaxdumpTARGZ		= sfle.d( pE, sfle.c_strDirTmp, "taxdump.tar.gz" )
c_fileProgTaxdump2TXT		= sfle.d( pE, sfle.c_strDirSrc, "taxdump2txt.py" )
c_fileProgTaxdump2Taxa		= sfle.d( pE, sfle.c_strDirSrc, "taxdump2taxa.py" )

#===============================================================================
# Shared data setup: NCBI taxonomy
#===============================================================================

sfle.download( pE, c_strURLTaxonomy, c_fileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strProg, strTARGZ = astrSs[:2]
	return sfle.ex( ("tar -xzOf", strTARGZ, "names.dmp nodes.dmp |" , strProg), strT )
Command( c_fileTaxdumpTXT, [c_fileProgTaxdump2TXT, c_fileTaxdumpTARGZ], funcTaxdumpTXT )

afileTaxIDs = sfle.pipe( pE, c_fileTaxdumpTXT, c_fileProgTaxdump2Taxa, c_fileTaxIDs,
	[[c_fileInputTaxa]] )

#===============================================================================
# Main SConscript on subdirectories
#===============================================================================

sfle.scons_children( pE, ".", afileTaxIDs, c_astrExclude )

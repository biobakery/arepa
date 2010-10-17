import sys
sys.path.append( "src" )
import arepa

c_strInputTaxa			= arepa.c_strEtc + "taxa"
c_fileTaxa				= File( arepa.c_strTmp + "taxids" )
c_strFileTaxdumpTXT		= arepa.c_strTmp + "taxdump.txt"
c_strFileTaxdumpTARGZ	= arepa.c_strTmp + "taxdump.tar.gz" 
c_strProgTaxdump2TXT	= arepa.c_strSource + "taxdump2txt.py"
c_strProgTaxdump2Taxa	= arepa.c_strSource + "taxdump2taxa.py"
Export( "c_fileTaxa" )

pE = Environment( )
Export( "pE" )

arepa.download( pE, c_strFileTaxdumpTARGZ,
	"ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz" )
pE.NoClean( c_strFileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "tar -xzOf " + astrSs[1] + " names.dmp nodes.dmp | " +
		astrSs[0], strT )
pE.Command( c_strFileTaxdumpTXT, [c_strProgTaxdump2TXT, c_strFileTaxdumpTARGZ],
	funcTaxdumpTXT )

arepa.pipe( pE, c_strFileTaxdumpTXT, c_strProgTaxdump2Taxa, c_fileTaxa,
	[[True, c_strInputTaxa]] )

astrDirs = filter( lambda p: ( type( p ) == type( Dir( "." ) ) ) and \
	( str(p) not in arepa.c_astrExclude ), Glob( "*" ) )
SConscript( dirs = astrDirs )

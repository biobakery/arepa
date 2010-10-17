import sys
import arepa

c_strInputTaxa			= arepa.c_strEtc + "taxa"
c_strFileTaxids			= arepa.c_strFileTaxids
c_strFileTaxdumpTXT		= arepa.c_strTmp + "taxdump.txt"
c_strFileTaxdumpTARGZ	= arepa.c_strTmp + "taxdump.tar.gz" 
c_strProgTaxdump2TXT	= arepa.c_strSource + "taxdump2txt.py"
c_strProgTaxdump2Taxa	= arepa.c_strSource + "taxdump2taxa.py"

pE = Environment( )

arepa.download( pE, c_strFileTaxdumpTARGZ,
	"ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz" )
pE.NoClean( c_strFileTaxdumpTARGZ )

def funcTaxdumpTXT( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	return arepa.ex( "tar -xzOf " + astrSs[1] + " names.dmp nodes.dmp | " +
		astrSs[0], strT )
pE.Command( c_strFileTaxdumpTXT, [c_strProgTaxdump2TXT, c_strFileTaxdumpTARGZ],
	funcTaxdumpTXT )

arepa.pipe( pE, c_strFileTaxdumpTXT, c_strProgTaxdump2Taxa, c_strFileTaxids,
	[[True, c_strInputTaxa]] )

for fileCur in Glob( "*" ):
	if ( type( fileCur ) != type( Dir( "." ) ) ) or \
		( str(fileCur) in arepa.c_astrExclude ):
		continue
	arepa.sconstruct( pE, fileCur )

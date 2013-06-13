"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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

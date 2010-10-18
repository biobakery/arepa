#!/usr/bin/env python

import arepa
import sys

if __name__ == "__main__":
	iLevel, strTo, strFrom = arepa.scons_args( sys.argv )
	sys.exit( 0 if ( iLevel == 1 ) else 1 )

pE = Environment( )
c_strID				= arepa.dir( pE )
c_strFileIDTXT		= c_strID + ".txt" 
c_strProgC2ID		= arepa.path_repo( pE ) + arepa.c_strSource + "c2id.py"
c_strFileIntactC	= arepa.path_repo( pE ) + arepa.c_strTmp + "intactc"

arepa.pipe( pE, c_strFileIntactC, c_strProgC2ID, c_strFileIDTXT, [[False, c_strID]] )

#!/usr/bin/env python

import arepa
import subprocess
import sys

if __name__ == "__main__":
	iLevel, strTo, strFrom = arepa.scons_args( sys.argv )
	if iLevel != 2:
		sys.exit( 1 )
	sys.exit( subprocess.call( "unzip -l " + strFrom + " | grep processed-data",
		shell = True ) )

pE = Environment( )
c_strID				= arepa.dir( pE )
c_strIDTXT			= ( Glob( "../*-processed-data-*.txt" ) or [""] )[0]
c_strIDPrePCL		= c_strID + "_pre.pcl"
c_strIDPCL			= c_strID + ".pcl"
c_strProgTXT2PCL	= arepa.path_repo( pE ) + arepa.c_strSource + "txt2pcl.rb"

#arepa.pipe( pE, c_strIDTXT, c_strProgTXT2PCL, c_strIDPrePCL,

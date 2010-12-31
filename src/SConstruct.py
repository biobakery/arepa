#!/usr/bin/env python

import arepa
import os
import sys

pE = Environment( )
c_afileSConscripts	= sorted( Glob( arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "SConscript*" ) ) )

if os.path.isfile( "SConscript" ):
	execfile( "SConscript" )
else:
	hashArgs = {}

# I tried very hard to do this using import, but I can't find a way to prematurely
# halt an import without sys.exit, which kills the entire process.
for fileSConscript in c_afileSConscripts:
	strSConscript = fileSConscript.get_abspath( )
	hashEnv = {"test" : lambda *a: False, "testing" : True}
	try:
		execfile( strSConscript, hashEnv )
	except SystemExit:
		pass
	if hashEnv["test"]( arepa.level( ), arepa.cwd( ), hashArgs ):
		execfile( strSConscript )

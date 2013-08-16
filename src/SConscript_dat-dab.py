#!/usr/bin/env python 
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

SConscript_dat-dab.py: 

shared code across modules 
handles all behavior pertaining to 
mapping dat to dab and generating quant files 
"""

import sfle
import arepa 

c_fileFlagSleipnir = sfle.d( pE, arepa.path_arepa( ), sfle.c_strDirEtc, "sleipnir" )

def funcDAB( pE, fileOutDAB, afileInDAT ):

	astrSleipnir = sfle.readcomment(c_fileFlagSleipnir)
	bSleipnir = ( astrSleipnir[0]=="True" ) 
	print "sleipnir", ("On" if bSleipnir else "Off")

	def _funcDAB( target, source, env ):
		strT, astrSs = sfle.ts( target, source )
		strOut, strMap = astrSs[:2]
		return sfle.ex( ("Dat2Dab", "-o", strT, "-i", ( strOut if sfle.isempty( strMap ) else strMap )) )

	if bSleipnir: 
		return pE.Command( fileOutDAB, afileInDAT, _funcDAB)


def funcPCL( pE, fileOutPCL, fileInPCL ):
	
	return sfle.sop( pE, "cp", [[fileInPCL], [True,fileOutPCL]] )

def funcQUANT( pE, fileQUANTin ):
	
	return sfle.scmd( pE, "echo '0.5\t1.5'", fileQUANTin ) 	

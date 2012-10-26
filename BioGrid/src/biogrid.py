#!/usr/bin/env python

import re
import csv
import sys


c_iColumns    = 15 

def split( strToken ):

    mtch = re.search( '^([^:]+):(.+)$', strToken )
    strType, strTmp = mtch.groups( ) if mtch else ("", strToken)
    mtch = re.search( '^(.+?)(?:\(([^)]+)\))?$', strTmp )
    strID, strGloss = mtch.groups( ) if mtch else (strTmp, "")
    
    return (strType, strID, strGloss)

def read( fileIntactC, strTarget, funcCallback, pArgs = None ):
    
    astrSymbols = []
    strID = fHit = None
    for strLine in fileIntactC:
        if strLine.startswith( ">" ):
            if fHit:
                break
            strID = strLine[1:].strip( )
        elif not strID:
            astrSymbols.append( strLine.strip( ) )
        elif strID == strTarget:
            fHit = True
            astrLine = strLine.strip( ).split( "\t" )
            if len( astrLine ) < c_iColumns:
                continue
            s = astrLine
            #sys.stderr.write("+++++++\n")
            #sys.stderr.write(str(s))
#            aArgs = [pArgs] + map( lambda s: astrSymbols[int(s)], [s[7], s[8], s[9], s[10], s[1], s[2], s[11], s[13], s[14], s[15], s[3], s[4],s[5],s[0], s[6]] )
            aArgs = [pArgs] + map( lambda s: astrSymbols [int(s)], [s[7],s[8], s[9], s[10], s[1],s[2], s[11], s[13], s[14],s[15], s[16], s[12], s[20],s[23], s[0]])    
            funcCallback( *aArgs )


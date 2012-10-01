#!/usr/bin/env python

import arepa
import re
import sys

c_repo = arepa.cwd()
c_strTaxid  = c_repo+"_taxid_"
c_strPMID    = "pmid_"
c_colTaxA = "Organism Interactor A"
c_colTaxB = "Organism Interactor B"
c_colGeneA = "Official Symbol Interactor A"
c_colGeneB = "Official Symbol Interactor B"
c_colPMID = "Pubmed ID"


def getColumnFromHeaderline (colnames, headerline):
    strLine = [strCur.strip( ) for strCur in headerline.split( "\t" )]
    colnumbers = []
    for col in colnames:
        l = [i for i,x in enumerate(strLine) if x==col]
        colnumbers.append(l[0])
    if colnumbers!=[]:
        return colnumbers
    else:
        return None


def symbol( hashSymbols, strValue ):
    return hashSymbols.setdefault( strValue, len( hashSymbols ) )




if len( sys.argv ) < 2:
    raise Exception( "Usage: bigrid2c.py <min> [taxa] < <biogrid.txt>" )

iMin = int(sys.argv[1])
strTaxa = None if ( len( sys.argv ) <= 2 ) else sys.argv[2]
setTaxa = arepa.taxa( strTaxa )
#sys.stderr.write( "\n".join([str(s) for s in setTaxa]) )  


hashSymbols = {}
hashhashPMTaxa = {}
for strLine in sys.stdin:
    if strLine and strLine[0].startswith( "#" ):
        cols = getColumnFromHeaderline([c_colPMID, c_colTaxA, c_colTaxB, c_colGeneA,c_colGeneB], strLine)
        continue
    strLine = [strCur.strip( ) for strCur in strLine.split( "\t" )]
    strPMID = strLine[int(cols[0])]
    strTax1 = strLine[int(cols[1])] 
    strTax2 = strLine[int(cols[2])]  

    #sys.stderr.write( strPMID +"\n" )
    #sys.stderr.write( strTax1 +"\n" )
    #sys.stderr.write( strTax2 +"\n" )

    if not strTax1 or ( strTax1 != strTax2 ):
        strTax1 = "0"
    if setTaxa and ( strTax1 not in setTaxa ):
        #sys.stderr.write( strTax1 + "\t" + "|".join([str(s) for s in setTaxa]) +"\n" )  
        continue
    #new_strLine = [ "pubmed:"+strPMID, "taxid:"+strTax1] + ["uniprotkb:"+s for s in strGenes] 
    hashhashPMTaxa.setdefault( strPMID, {} ).setdefault( strTax1, [] ).append(
        [symbol( hashSymbols, strCur ) for strCur in strLine] )


aaSymbols = sorted( hashSymbols.items( ), cmp = lambda aOne, aTwo: cmp( aOne[1], aTwo[1] ) )
print( "\n".join( aCur[0] for aCur in aaSymbols ) )

hashBins = {}
for strPMID, hashTaxa in hashhashPMTaxa.items( ):
    for strTaxon, aaiLines in hashTaxa.items( ):
        strTaxid = c_strTaxid + strTaxon
        strBin = strTaxid + ( "" if ( ( not strPMID ) or ( len( aaiLines ) < iMin ) ) else \
                ( "_" + c_strPMID + strPMID ) )
        hashBins.setdefault( strBin, [] ).extend( aaiLines )
        #hashBins.setdefastrLine[:c_iColumns].Default( strBin, [] ).extend( aaiLines )

for strBin, aaiLines in hashBins.items( ):
    print( ">" + strBin )
    for aiLine in aaiLines:
        print( "\t".join( str(i) for i in aiLine ) )

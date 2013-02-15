#!/usr/bin/env python
'''
Main script for genemapper 
'''

import arepa 
import sfle 
import glob 

c_strDirMapping 	= sfle.d( arepa.path_repo(), sfle.c_strDirEtc, "uniprotko" )
c_strFileManualMapping	= sfle.d( arepa.path_repo(), sfle.c_strDirEtc, "manual_mapping.txt" )

########## General Mapping Functions ###########

def get_mappingfile( strTaxID, fApprox = True, strDir = c_strDirMapping ):
        if not(strTaxID):
                return None
        elif not(sfle.isempty(c_strFileManualMapping)):
		
	else:
		if not(sfle.isempty(c_strFileManualMapping)):
			pHash = {k:v for k,v in csv.reader(open(c_strFileManualMapping), csv.excel_tab)}
			astrMapOutTmp = filter(bool,[pHash.get(item) for item in taxid2org( strTaxID, True )])
			astrMapOut = map(lambda x: sfle.d( c_strDirMapping, x), astrMapOutTmp) if astrMapOutTmp else []
		if not(astrMapOut):
			astrIDs = [strTaxID] if not(fApprox) else org2taxid( taxid2org( strTaxID ), True )
			for strID in astrIDs:
				astrGlob =  glob.glob( sfle.d( strDir, strID + "_*" ) )
				if astrGlob:
					astrMapOut = astrGlob
					break
                return (astrMapOut[0] if astrMapOut else None)


if __name__ == '__main__':
	pass 

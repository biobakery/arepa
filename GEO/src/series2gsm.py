#!/usr/bin/env python

import csv
import sys
import re
import sfle
import arepa
import ftplib

c_strURLGEO					= 'ftp.ncbi.nih.gov'
c_strURLGEOsupp					= 'pub/geo/DATA/supplementary/samples/'
c_strURLSupp 					= 'ftp://' + c_strURLGEO + '/' + c_strURLGEOsupp 
c_strFileGSM					= "../GSM.txt"

def nnnModify( strID ):
	return strID[0:len(strID)-3] + "nnn/"

def funcGetGSMids( ):
	dummylist = []
	for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
		if not ( astrLine and astrLine[0] and ( astrLine[0][0] == "!" ) ):
			continue
		strFrom = astrLine[0][1:]
		if strFrom == 'Sample_geo_accession':
			#print( "\n".join( astrLine[1:]  ) )
			return astrLine[1:]

def funcRAWCEL( listGSM ):
	dummylist = []
	listGSM = listGSM
	for GSMid in listGSM:
			strURLGSM		= nnnModify( GSMid ) + GSMid
			strURLGSMftpbase	= c_strURLGEOsupp + strURLGSM
			listFiles		= sfle.ftpls( c_strURLGEO, strURLGSMftpbase ) 	
			dummylist += listFiles 

	clistFiles = dummylist
	def celFilter( list ):
		dummylist = []
		for item in list:
			if 'CEL' in item:
				dummylist.append( str(item) )
			else:
				dummylist.append( "#" + str(item) )
		return dummylist
	return celFilter( clistFiles )	

#Execute 
c_listGSM = funcGetGSMids( )
c_listCEL = funcRAWCEL ( c_listGSM )
print("\n".join( c_listCEL ) )

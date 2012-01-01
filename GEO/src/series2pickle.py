#!/usr/bin/env python 

import csv
import pickle
import re
import sys

c_strKeyCuration	= "curation"
c_strKeyMCSM		= "manually_curated_sample_metadata"

key = {
	'pubmed_id'		:'pmid',
	'title'			:'title', 
	'summary'		:'gloss', 
	'type'			:'type', 
	'channel_count'	:'channels',
	'platform_id'	:'platform', 
	'sample_taxid'	:'taxid', 
	'sample_count'	:'conditions'
}

manual_key = {
	"platform title"		: "platform_title", 
	"citation"				: "citation", 
	"sample history"		: "sample_history", 
	"sample handling"		: "sample_handling", 
	"sample type"			: "sample_type", 
	"sample preservation"	: "sample_preservation",
	"platform_manufacturer"	: "platform_manufacturer", 
	"platform distribution"	: "platform_distribution", 
	"platform accession"	: "platform_accession", 
	"technology type"		: "technology_type", 
	"geneSigDB signatures"	: "geneSigDB_signatures"
} 

catalog = ['title', 'type', 'summary', 'sample_taxid', 'channel_count', 'platform_id', 'pubmed_id', 'sample_count' ] 

manual_sample_keys = ['sample_name', 'sample_type', 'subtype', 'primarysite', 'arrayedsite', 'summarygrade', 'summarystage', 'T', 'substage', 'G', 'N', 'M']

def modify(_list_):
	content = re.findall('".+"', _list_[0])
	return re.sub('"', '', content[0])

def ID(strID, strg, inputFile):
	f = inputFile
	if strg == 'pubmed_id': 
		return re.findall(r'Series_pubmed_id.*', f)
	if strg == 'title': 
		return re.findall(r'Series_title.*', f)
	if strg == 'summary': 
		return re.findall(r'Series_summary.*',f)
	if strg == 'type': 
		return re.findall(r'Series_type.*',f)
	channel_count = re.findall(r'Sample_channel_count.*',f)
	count_column = re.findall(r'\d', channel_count[0])
	if strg == 'channel_count':
		return ['"' + count_column[0] + '"']
	if strg == 'platform_id':
		if len( strID.split("-")) == 1:
			return re.findall(r'Series_platform_id.*',f)
		else:
			return ['"' + strID.split("-")[1] + '"']
	if strg == 'sample_taxid':
		return re.findall(r'Series_sample_taxid.*',f)
	sample_id = re.findall(r'"ID_REF".*',f)
	GSM_ids = re.findall(r'GSM\d+' , modify(sample_id))
	if strg == 'sample_count':
		return ['"' + str(len(GSM_ids)) + '"']

def printformat(strID, strFileManCurData, catalog, key, seriesFile, outputDict = None):
	if not outputDict:
		outputDict = {}
	for strg in catalog:
		header = key[strg]
		description  = str(modify(ID(strID, strg, seriesFile)))		
		outputDict[header] = description 
	if strFileManCurData:
		astrKeys = None
		for astrLine in csv.reader( open( strFileManCurData ), csv.excel_tab ):
			if astrKeys:
				for i in range( len( astrLine ) ):
					outputDict.setdefault( astrKeys[i], [] ).append( astrLine[i] )
			else:
				astrKeys = astrLine
		outputDict[ c_strKeyCuration ] = astrKeys
	return outputDict

def grab_sample_curated_data( strID, ManCurDataID ):
		
	def populate_manual_sample_keys( ):
		dictR = csv.DictReader(open( ManCurDataID, 'rb'), delimiter='\t') 
		for item in dictR:
			return item.keys()
		
	def adder( dictR, key ):
		dummylist = []
		for item in dictR:
			dummylist.append(item[key])
		return dummylist
	 
	def populate_dummydictR( dummydictR = None ):
		if not dummydictR:
			dummydictR = []
		for item in csv.DictReader(open( ManCurDataID, 'rb'), delimiter='\t'):
			dummydictR.append(item)
		return dummydictR
	dummydictR = populate_dummydictR( )

	dummydict = {}
	for key in populate_manual_sample_keys( ):
		dummydict[key] = adder( dummydictR, key )
	dummydict[ c_strKeyMCSM ] = dummydict.keys()
	return dummydict

def decider( strID, strMetadata, catalog, key, seriesFile ):
	outputDict = printformat(strID, strMetadata, catalog, key, seriesFile)
	if strMetadata:
		manualDict = grab_sample_curated_data( strID, strMetadata )
		outputDict.update(manualDict)	
	pickle.dump( outputDict, sys.stdout, -1 )

if len( sys.argv ) < 2:
	raise Exception( "Usage: series2pickle.py <id> [curated.txt] < <series.txt>" )
strID = sys.argv[1]
strMetadata = sys.argv[2] if ( len( sys.argv ) > 2 ) else None

# BUGBUG: this slurps the whole thing into memory; ugh
decider(strID, strMetadata, catalog, key, sys.stdin.read( ))

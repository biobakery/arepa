#!/usr/bin/env python 

import pickle
import sys
import re
import os
import arepa 
import csv
import glob

c_strID			= arepa.cwd()
c_strFileManCurData	= arepa.d( arepa.path_repo( ), arepa.c_strDirEtc, "manual_curation/", "ovarian_cancer_public_datasets.csv" )
c_strOutputPickle 	= c_strID + ".pkl" 
c_strDirManCur 		= arepa.d( arepa.path_repo( ), arepa.c_strDirEtc, "manual_curation/" )
c_strKeyCuration	= "curation"
c_strKeyMCSM		= "manually_curated_sample_metadata"


key = {	
	'pubmed_id'	:'pmid',
	'title'		:'title', 
	'summary'	:'gloss', 
	'type'		:'type', 
	'channel_count'	:'channels',
	'platform_id'	:'platform', 
	'sample_taxid'	:'taxid', 
	'sample_count'	:'conditions'
	 }

manual_key = {
	"platform title"	: "platform_title", 
	"citation"		: "citation", 
	"sample history"	: "sample_history", 
	"sample handling"	: "sample_handling", 
	"sample type"		: "sample_type", 
	"sample preservation"	: "sample_preservation",
	"platform_manufacturer"	: "platform_manufacturer", 
	"platform distribution"	: "platform_distribution", 
	"platform accession"	: "platform_accession", 
	"technology type"	: "technology_type", 
	"geneSigDB signatures"	: "geneSigDB_signatures"
	} 

catalog = ['title', 'type', 'summary', 'sample_taxid', 'channel_count', 'platform_id', 'pubmed_id', 'sample_count' ] 

manual_sample_keys = ['sample_name', 'sample_type', 'subtype', 'primarysite', 'arrayedsite', 'summarygrade', 'summarystage', 'T', 'substage', 'G', 'N', 'M']

def meta_decider( strID ):
        '''Decides if manually curated metadata exists for the ID'''
	item_list = glob.glob( c_strDirManCur + strID + "*" )
        if len( item_list ) != 0:
                return item_list[0]
        else:
                return None

def modify(_list_):
	content = re.findall('".+"', _list_[0])
	return re.sub('"', '', content[0])

def ID(strg, inputFile):
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
		if len( arepa.cwd().split("-")) == 1:
			return re.findall(r'Series_platform_id.*',f)
		else:
			return ['"' + arepa.cwd().split("-")[1] + '"']
	if strg == 'sample_taxid':
		return re.findall(r'Series_sample_taxid.*',f)
	sample_id = re.findall(r'"ID_REF".*',f)
	GSM_ids = re.findall(r'GSM\d+' , modify(sample_id))
	if strg == 'sample_count':
		return ['"' + str(len(GSM_ids)) + '"']

def printformat(catalog, key, seriesFile, outputDict = None):
	if not outputDict:
		outputDict = {}
	for strg in catalog:
		header = key[strg]
		description  = str(modify(ID(strg, seriesFile)))		
		outputDict[header] = description 
	if c_strID in arepa.csvread( c_strFileManCurData ):
		manref = arepa.csvread( c_strFileManCurData )
		rev_manual_key = dict((v,k) for k,v in manual_key.items())
		for item in manual_key.values():
			outputDict[rev_manual_key[item]] = manref[c_strID][item]
		outputDict[ c_strKeyCuration ] = manual_key.keys()
	else:
		pass 		
	return outputDict

def grab_sample_curated_data( c_strID, dummylist = None, dummydict = None ):
        
	ManCurDataID = meta_decider( c_strID ) 
		
	def populate_manual_sample_keys( ):
		dictR = csv.DictReader(open( ManCurDataID, 'rb'), delimiter='\t') 
		for item in dictR:
			return item.keys()
			break	

	if not dummydict:
                dummydict = {}
        
        def adder( dictR, key, dummylist = None ):
                if not dummylist:
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
	for key in populate_manual_sample_keys( ):
		dummydict[key] = adder( dummydictR, key )
	dummydict[ c_strKeyMCSM ] = dummydict.keys()
        return dummydict


def decider( c_strID, catalog, key, seriesFile ):
	outputDict = printformat(catalog, key, seriesFile)
	if not meta_decider( c_strID ): 
		pass
	else:
		manualDict = grab_sample_curated_data( c_strID )
		outputDict.update(manualDict)	
	with open( c_strOutputPickle, "wb" ) as outputf:
		pickle.dump( outputDict, outputf )
		
	

## Execute 
decider(c_strID, catalog, key, sys.stdin.read( ))



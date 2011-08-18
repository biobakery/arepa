#!/usr/bin/env python 

import sys
import re
import os
import arepa 

c_strID			= arepa.cwd()
c_strFileManCurData	= arepa.d( arepa.path_repo( ), arepa.c_strDirEtc, "manual_curation/", "ovarian_cancer_public_datasets.csv" )

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

def printformat(catalog, key, seriesFile):
	for strg in catalog:
		header = key[strg]
		description  = str(modify(ID(strg, seriesFile)))
		sys.stdout.write(header)
		sys.stdout.write('\t')
		sys.stdout.write(description)
		sys.stdout.write('\n')
	if c_strID in arepa.csvread( c_strFileManCurData ):
		manref = arepa.csvread( c_strFileManCurData )
		rev_manual_key = dict((v,k) for k,v in manual_key.items())
		for item in manual_key.values():
			sys.stdout.write(rev_manual_key[item])
			sys.stdout.write('\t')
			sys.stdout.write(str(manref[c_strID][item]))
			sys.stdout.write('\n')
		sys.stdout.write('curation')
		sys.stdout.write('\t')
		sys.stdout.write(str(manual_key.keys()))
		sys.stdout.write('\n')
	else:
		pass 		
			
## Execute 
printformat(catalog, key, sys.stdin.read( ))


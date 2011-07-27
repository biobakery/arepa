#!/usr/bin/env python 

import sys
import re
import os

key = {'pubmed_id': 'pmid', 'title': 'title', 'summary': 'gloss', 'type':'type', 'channel_count': 'channels',
	'platform_id': 'platform', 'sample_taxid': 'taxid', 'sample_count': 'conditions' }
catalog = ['title', 'type', 'summary', 'sample_taxid', 'channel_count', 'platform_id', 'pubmed_id', 'sample_count' ] 

def modify(_list_):
	content = re.findall('".+"', _list_[0])
	return re.sub('"', '', content[0])

def ID(strg, inputFile):
	f = inputFile
	if strg == 'pubmed_id': 
		return re.findall('Series_pubmed_id.*', f)
	if strg == 'title': 
		return re.findall('Series_title.*', f)
	if strg == 'summary': 
		return re.findall('Series_summary.*',f)
	if strg == 'type': 
		return re.findall('Series_type.*',f)
	channel_count = re.findall('Sample_channel_count.*',f)
	count_column = re.findall('\d', channel_count[0])
	if strg == 'channel_count':
		return ['"' + count_column[0] + '"']
	if strg == 'platform_id':
		return re.findall('Series_platform_id.*',f)
	if strg == 'sample_taxid':
		return re.findall('Series_sample_taxid.*',f)
	sample_id = re.findall('Series_sample_id.*',f)
	GSM_ids = re.findall('GSM\d+\s*' , modify(sample_id))
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
	
## Execute 
printformat(catalog, key, sys.stdin.read( ))


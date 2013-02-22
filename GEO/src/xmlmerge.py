#!/usr/bin/env python

import sfle 
import sys 
import subprocess

c_strType                       = "type"
c_strCount                      = "count"
c_strQuery                      = "query_key"
c_strWebEnv                     = "WebEnv"
c_iIncrement 			= 10000
c_iRetMax			= 1000000
c_strSufXML			= ".xml"
c_strURLSum                     = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&retstart=%s&retmax=1000000&query_key=%s&WebEnv=%s"

if len( sys.argv[1:] ) !=2:
	raise Exception("Usage: xmlmerge.py <metadata> <id>" )	

inputf, geo_id  = sys.argv[1:]
hashRet = {k:v for k,v in map( lambda s: s.split("\t"), sfle.readcomment( open( inputf ) ))}
id_count, query_key, web_env =  [hashRet.get(i) for i in [ c_strCount, c_strQuery, c_strWebEnv]]

#===========================================================================
# Iteratively download temporary xml files 
#===========================================================================

def discrete_list( num, increment ):
    iTries = ( num / increment ) + 1
    return [str( 1 + ( a * increment ) ) for a in range( iTries )]

count_list =  discrete_list( int(id_count), c_iIncrement )
astrOutput = [sfle.d(sfle.c_strDirTmp,geo_id + str(i) + c_strSufXML) for i in range(1,len(count_list)+1)] 
query_list = zip( astrOutput, count_list, [query_key] * len(count_list), [web_env] * len(count_list) ) 

# Download 
for astr in query_list:
	strT, strCount, strQuery, strWeb = astr 
	sfle.ex( ["curl", "-g", "-f", "-z", '"' + strT +  '"', '"' + c_strURLSum % (strCount,strQuery,strWeb) + '"', ">", strT] )

#Save 
with open( sfle.d(sfle.c_strDirTmp,geo_id + c_strSufXML), "w" ) as idXML:
	idXML.write( "\n".join( [open( f ).read() for f in zip(*query_list)[0]] ) )
	

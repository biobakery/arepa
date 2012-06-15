import sfle 
import glob
import csv  
import sys 
import re 

''' parse mapping files
begins with !platform_table_begin 
ends with !platform_table_end '''
print sys.argv
strGPL, strMap = sys.argv[1:3]

c_hashHead = 	{
		r"^ID"				: "Affy",	
		r"^Gene Symbol"			: "HGNC", 
		r"^Uniprot .*? Symbol"		: "Unitprot/TrEMBL", 
		r"^UniGene .*? Symbol"		: "Unigene",
		r"^Entrez .*? Symbol"		: "EntrezGene"
		} 

#do I read in from a text file, just like in GSM?
#for testing purposes 

strGPLID = True 
if strGPLID:
	aHead = re.findall(r"^#(.+?)\n", open( strGPL,"r" ).read(),re.MULTILINE )
	aKeys, aDesc = zip(*map( lambda v: map(lambda w: w.strip(), v.split("=")), aHead )) 
	aOutKeys = [] 
	hOutDict = {}
	for item in c_hashHead.keys():
		for desc in aDesc:
			reLine = re.findall(item, desc, re.M|re.I)
			if reLine:
				aOutKeys.extend( [aKeys[aDesc.index(desc)]] )
				hOutDict[reLine[0]] = c_hashHead[item] 	
	print str(aOutKeys)
	print str(hOutDict)
	strTable = re.findall(r"!platform_table_begin(.+)!platform_table_end", \
		open( strGPL ).read(), re.S )[0].strip()
	dr = csv.DictReader( strTable.split("\n"), delimiter = "\t" ) 
	with open( strMap, "w" ) as outputf:
		print "writing..."
		outputf.write( "\t".join( aOutKeys ) + "\n" )
		for item in dr:
			try:
				outputf.write( "\t".join( [item[k] for k in aOutKeys] ) + "\n" )
			except KeyError:
				continue  
		print "done!"
else:
	with open( strMap, "w" ) as outputf:
		outputf.write("") 

#!/usr/bin/env python
'''
Main gene mapping python script
'''

#~/dboernig/arepa/GeneMapper/src/bridgemapper.py ~/dboernig/arepa/STRING/data/taxid_100226_mode_binding/taxid_100226_mode_binding.dat ~/dboernig/arepa/STRING/data/taxid_100226_mode_binding/tester.dat ~/dboernig/arepa/STRING/etc/100226_sco_ko_uniprot.map [0] Kg Ck

import sys
import csv
import pickle
import sfle
import arepa
import os
import metadata 
import sets 

if len( sys.argv ) < 7:
        raise Exception( "Usage: bridgemapper.py <inputfile.dat> <outputfile.dat> \
			<mappingfile> <columnlist in inputfile to be mapped> \
			<input system code for bridgemapper> \
			<output system code for bridgemapper> [rows skipped]" )

c_inputfile 		= sys.argv[1]
c_outputfile 		= sys.argv[2]
c_mappingfilein 	= sys.argv[3]
c_columnToMap 		= list(sys.argv[4])
c_origGeneId 		= sys.argv[5]
c_destGeneId 		= sys.argv[6]
c_fileStatus		= sys.argv[7]
c_iRowSkip 		= int(sys.argv[8]) if (len(sys.argv[1:]) > 7 and sys.argv[8]) else 0  

#Remove the delimiter from the list of strings so that we end up with only the acutal columns in the list:
c_columnToMap = filter( lambda a: a != ",", c_columnToMap[1:-1] )

c_generatorNum		= (i for i in range(1,len(c_columnToMap)+1))

c_path_GeneMapper 	= sfle.d( arepa.path_arepa(), "GeneMapper")
c_path_geneidmapper 	= sfle.d(c_path_GeneMapper, "trunk", "batchmapper.sh")
c_mappingfile 		= c_mappingfilein 
c_path_mappingfiles 	= os.path.dirname(c_mappingfile)
c_path_inputfile	= os.path.dirname(c_inputfile)

if c_mappingfile.endswith(".bridge"):
	c_mappingflag = "-g"
elif c_mappingfile.endswith(".txt") or c_mappingfile.endswith(".map"):
	c_mappingflag = "-t"

#########################################################
# Local functions
#########################################################

#Gets a specific column from a table file
def readColFromTable (table,ind):
	fullcolumn = []
	columns = csv.reader(open(table),delimiter="\t")
	[fullcolumn.append(col[ind]) for col in columns]
	return fullcolumn

#Reads complete table file into a list
def readTable(table):
	content = []
	f = csv.reader(open(table),delimiter="\t")
	[content.append(col) for col in f]
	return content

#Transpose a given matrix
def transpose(matrix):
	return [[matrix[x][y] for x in range(len(matrix))] for y in range(len(matrix[0]))]

#Saves a column vector as a file
def saveColumnAsTxtFile (col, txtfile):
	f = open(txtfile, 'w')
	f.writelines(["%s\n" % item for item in col])
	f.close()

#Saves a PCL file as a file
def savePCLAsTxtFile (txtfile, content):
	with open(txtfile, 'w') as outfile:
		outfile.writelines('\t'.join(i) + '\n' for i in content)
    
#Write Empty file in error case to avoid trouble with scons:
def writeEmptyFile(txtfile):
	f=open(txtfile,"w")
	f.write("")
	f.close()

#########################################################
# GENE ID MAPPING: convert geneids_in into geneids_out
#########################################################
def convertGeneIds (geneids, mapfile):
	#iCol = next(c_generatorNum)
	inputfile = sfle.d(c_path_mappingfiles, 'geneids.txt') 
	#inputfile = sfle.d(c_path_inputfile, 'geneids' + str(iCol) + '.txt')
	#outputfile = sfle.d(c_path_inputfile, 'geneids' + str(iCol) + '_mapped.txt')	
	outputfile = sfle.d(c_path_mappingfiles, 'geneids_mapped.txt') 
	saveColumnAsTxtFile (geneids, inputfile)
	sfle.ex([c_path_geneidmapper, " -i ", inputfile, " -is",c_origGeneId , \
		" -os ",c_destGeneId, " -o ",outputfile, c_mappingflag , mapfile ," -mm "])
	hashOut = {k:v for v,k in readTable(outputfile)}
	return hashOut 

def listfirstitem (l): return l[0]

##################################################################
# Replace the probe set ids in the pcl file with the new gene ids
##################################################################
def replaceGeneIdsInPCLMatrix (matrix, vec, col):
	matrix_out = matrix
	matrix_out[col] = vec
	return matrix_out

#########################################################
# Handling NxM geneids 
#########################################################
def handleNxMgenes(matrix_in, pattern):
	matrix_out = []
	iCol = len(matrix_in[0])
	for row in matrix_in:
		crow = row
		#gene = crow[col]
		for i in range(iCol):
			gene = crow[i]
			if gene.find(pattern) != -1:
				break
			elif gene.strip() == "":  
				break
			elif i== (iCol-1):
				matrix_out.append(row)
			else:
				continue 
	return matrix_out

      
###########################################################
# Getting the probe set ids from the pcl file: geneids_in 
###########################################################

#Open a blank metadata object
hashMeta = metadata.open()

if os.path.exists(c_inputfile) and os.stat(c_inputfile)[6]!=0:
        if os.path.exists(c_mappingfile) and os.stat(c_mappingfile)[6]!=0:
                table_header, table_in = readTable(c_inputfile)[:c_iRowSkip], readTable(c_inputfile)[c_iRowSkip:]
                table_in_columns = len(table_in[0])
                if table_in_columns >= len(c_columnToMap):
                        table_in_transp = zip(*table_in)
                        columns_to_map = [list(table_in_transp[int(i)]) for i in c_columnToMap]
                        names_to_map = set(reduce(lambda x,y: x+y,columns_to_map,[])) 
                        astrNames = [x for x in names_to_map]
                        hashMap = convertGeneIds(astrNames,c_mappingfile)
                        table_geneids_replaced = zip(*[map(lambda x: hashMap[x] if any(hashMap[x]) else x \
				,table_in_transp[iCol]) if str(iCol) in c_columnToMap else table_in_transp[iCol] \
                                for iCol in range(len(table_in_transp))])
			table_out = table_header + table_geneids_replaced if any(table_header) else \
				table_geneids_replaced
                        if any(table_out):    
                                savePCLAsTxtFile(c_outputfile,table_out)
                                hashMeta.update({"mapped":True})
                        else:
                                sys.stderr.write("+++Error in GeneMapper +++ Empty mapping. \
                                        Return original file. \n")      
                                savePCLAsTxtFile( c_outputfile, readTable(c_inputfile) )
                                hashMeta.update({"mapped":False})       
                else:
                        sys.stderr.write(" +++ ERROR in GeneMapper +++ Number of requested columns to \
				map is larger than the number of columns in the input data file.\n")
                        savePCLAasTxtFile( c_outputfile, readTable(c_inputfile))
                        hashMeta.update({"mapped":False})
        else:
                sys.stderr.write("+++ ERROR in GeneMapper +++ Mapping file does not exist or is empty. \
                        Return original file. \n")
                savePCLAsTxtFile( c_outputfile, readTable(c_inputfile) )
                hashMeta.update({"mapped":False})
else:
        sys.stderr.write("+++ ERROR in GeneMapper +++ Input file does not exist or is empty. \
                Return empty file. \n")
        savePCLAsTxtFile( c_outputfile, readTable(c_inputfile) )
        hashMeta.update({"mapped":False})

#Save Metadata
if c_fileStatus!="None":
	with open( c_fileStatus, "w" ) as outputf:
		outputf.write( "\t".join( ["mapped",str(hashMeta.get("mapped"))] ) )

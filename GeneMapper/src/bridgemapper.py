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

if len( sys.argv ) < 7:
        raise Exception( "Usage: bridgemapper.py <inputfile.dat> <outputfile.dat> \
			<mappingfile> <columnlist in inputfile to be mapped> \
			<input system code for bridgemapper> \
			<output system code for bridgemapper>" )

c_inputfile 		= sys.argv[1]
c_outputfile 		= sys.argv[2]
c_mappingfilein 	= sys.argv[3]
c_columnToMap 		= list(sys.argv[4])
c_origGeneId 		= sys.argv[5]
c_destGeneId 		= sys.argv[6]
c_fileStatus		= sys.argv[7]

#Remove the delimiter from the list of strings so that we end up with only the acutal columns in the list:
c_columnToMap = filter( lambda a: a != (" " or "," or ";"), c_columnToMap[1:-1] )

c_path_GeneMapper 	= sfle.d( arepa.path_arepa(), "GeneMapper")
c_path_geneidmapper 	= sfle.d(c_path_GeneMapper, "trunk", "batchmapper.sh")
c_mappingfile 		= c_mappingfilein 
c_path_mappingfiles 	= os.path.dirname(c_mappingfile)

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
    with open(txtfile, 'w') as file:
        file.writelines('\t'.join(i) + '\n' for i in content)
    
#Write Empty file in error case to avoid trouble with scons:
def writeEmptyFile(txtfile):
    f=open(txtfile,"w")
    f.write("")
    f.close()

#########################################################
# GENE ID MAPPING: convert geneids_in into geneids_out
#########################################################
def convertGeneIds (geneids, mapfile):
    inputfile = sfle.d(c_path_mappingfiles, 'geneids.txt') 
    outputfile = sfle.d(c_path_mappingfiles, 'geneids_mapped.txt') 
    saveColumnAsTxtFile (geneids, inputfile)
    sfle.ex([c_path_geneidmapper, " -i ", inputfile, " -is",c_origGeneId , \
	" -os ",c_destGeneId, " -o ",outputfile, c_mappingflag , mapfile ," -mm "])
    return readTable(outputfile)

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
def handleNxMgenes (matrix_in, pattern, col):
    matrix_out = []
    for row in matrix_in:
        crow = row
        gene = crow[col]
        if gene.find(pattern) != -1:
            continue
        elif gene == "":  
            continue
        else:
            matrix_out.append(crow)
    return matrix_out
    
def handleDoubleEntries (matrix_in):
    vec = []
    vec2 = []
    vec22=[]
    matrix_out=[]
    pattern = "___"
    #formatting matrix into simple vector:
    for row in matrix_in:
        vec.append(pattern.join(row))
        vec2.append(pattern.join([row[1], row[0]]))
        vec22.append(pattern.join(row[:2]))
    for i,v in enumerate(vec):
        for j,v2 in enumerate(vec2):
            if v2 in v:
                vec[j] = ""
        for jj,v22 in enumerate(vec22):
            if i != jj:
               if v22 in v:
                   vec[jj] = ""
    vec = filter(None,vec)
    #remove equal entries:
    vec = list(set(vec)) 
    #reformatting into a matrix:
    for v in vec:
        matrix_out.append(v.split(pattern))
    return matrix_out


###########################################################
# Getting the probe set ids from the pcl file: geneids_in 
###########################################################

#Open a blank metadata object
hashMeta = metadata.open()

#Map
if os.path.exists(c_inputfile) and os.stat(c_inputfile)[6]!=0:
    if os.path.exists(c_mappingfile) and os.stat(c_mappingfile)[6]!=0:
        table_in = readTable(c_inputfile)
        table_in_columns = len(table_in[0])
        if table_in_columns > len(c_columnToMap):
            for col in c_columnToMap:
                if table_in != []:
                    col = int(col)
                    table_in_transp = transpose(table_in)
                    geneids_in = table_in_transp[col]
                    geneids_out_tmp = convertGeneIds (geneids_in, c_mappingfile)
                    geneids_out = map(listfirstitem, geneids_out_tmp)
                    table_geneids_replaced = transpose(replaceGeneIdsInPCLMatrix \
			(table_in_transp,geneids_out, col))
                    ## Handling NxM entry gene names from BridgeDB:
                    table_out_tmp = handleNxMgenes(table_geneids_replaced, " /// ", col)
                    #table_out = handleDoubleEntries(table_out_tmp)
                    table_out = table_out_tmp
                    table_in = table_out
                else:
                    sys.stderr.write( "+++ ERROR in GeneMapper +++ Empty mapping. Return original file.\n")
		    savePCLAsTxtFile( c_outputfile, readTable( c_inputfile ) )
		    hashMeta.update({"mapped": False})
                    break
            if table_out != []:
                savePCLAsTxtFile (c_outputfile, readTable( c_inputfile)[:2] + table_out)
		hashMeta.update({"mapped":True})
            else:
                sys.stderr.write( "+++ ERROR in GeneMapper +++ Empty output mapping. Return original file.\n")
		savePCLAsTxtFile( c_outputfile, readTable( c_inputfile ) )
		hashMeta.update({"mapped":False})
        else:
            sys.stderr.write( "+++ ERROR in GeneMapper +++ Number of requested columns to map is \
		larger than the number of columns in the input data file.\n")
	    savePCLAsTxtFile( c_outputfile, table_in )
	    hashMeta.update({"mapped":False})
    else:
        sys.stderr.write("+++ ERROR in GeneMapper +++ Mapping file does not exist or is empty. \
		Return original file.\n")               
	savePCLAsTxtFile( c_outputfile, readTable( c_inputfile ) )
	hashMeta.update({"mapped":False})
else: 
    sys.stderr.write( "+++ ERROR in GeneMapper +++ Input file does not exist or is empty. \
	Return empty file.\n")
    savePCLAsTxtFile( c_outputfile, readTable( c_inputfile ) )
    hashMeta.update({"mapped":False})

#Save Metadata
with open( c_fileStatus, "w" ) as outputf:
	outputf.write( "\t".join( ["mapped",str(hashMeta.get("mapped"))] ) )

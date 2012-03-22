#!/usr/bin/env python

# in arepa: export PYTHONPATH=`pwd`/../sfle/src:`pwd`/src
# CALL: python ../pclids.py GSE8218_00raw.pcl GSE8218_00mapped.pcl ~/dboernig/arepa/src/test/GPL96_taxid9606.txt


import sys
import csv
import pickle
import sfle
import arepa
import os


#c_pkl_metadatafile = sys.stdin
c_pcl_inputfile = sys.argv[1]
c_pcl_outputfile = sys.argv[2]
c_mappingfile = sys.argv[3]

c_path_geneidmapper = "/home/dboernig/dboernig/BridgeDB/bridgedb/batchmapper.sh"
c_path_mappingfiles = os.path.dirname(c_mappingfile)



#########################################################
# Local functions
#######################################################

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
    

#########################################################
# GENE ID MAPPING: convert geneids_in into geneids_out
#########################################################
#The actual converting function, in the future it should call arepa.geneid, now it still calls batchmapper from commandline.
def convertGeneIds (geneids_in, mappingfile):
    inputfile = sfle.d(c_path_mappingfiles, 'geneids.txt') 
    outputfile = sfle.d(c_path_mappingfiles, 'geneids_mapped.txt') 
    saveColumnAsTxtFile (geneids_in, inputfile)
    sfle.ex([c_path_geneidmapper, " -i ", inputfile, " -is X -os H -o ",outputfile, " -t ", mappingfile ," -mm "])
    return readTable(outputfile)


def listfirstitem (l): return l[0]


#########################################################
# Replace the probe set ids in the pcl file with the new gene ids
#########################################################

def replaceGeneIdsInPCLMatrix (pcl_in, geneids_out):
    pcl_out = pcl_in
    pcl_out[0] = geneids_out
    return pcl_out


#########################################################
# Handling NxM geneids 
#########################################################
def handleNxMgenes (matrix_in, pattern):
    matrix_out = []
    header = range(2)
    i=0
    for row in matrix_in:
        crow = row
        if i not in header:
            gene = crow[0]
            if gene.find(pattern) != -1:
                continue
                #ngenes = gene.split(pattern)
                #for j in range(len(ngenes)):
                #    row_ngenes = crow
                #    row_ngenes[0] = str(ngenes[j])
                #    matrix_out.append(list(row_ngenes))
            elif gene == "":  
                continue
            else:
                matrix_out.append(crow)
        else:
            matrix_out.append(crow)
        i+=1  
    return matrix_out
    

#########################################################
# Getting the probe set ids from the pcl file: geneids_in 
########################################################
pcl_in = readTable(c_pcl_inputfile)
pcl_in_transp = transpose(pcl_in)
geneids_in = pcl_in_transp[0]


#########################################################
# Do the acutal gene id mapping if mappingfile exists: 
########################################################
if os.path.exists(c_mappingfile):
    geneids_out_tmp = convertGeneIds (geneids_in, c_mappingfile)
    geneids_out = map(listfirstitem, geneids_out_tmp)
    #copy the 2 column header from the original file to the new file:
    geneids_out[0], geneids_out[1] = geneids_in[0], geneids_in[1]
    pcl_geneids_replaced = transpose(replaceGeneIdsInPCLMatrix (pcl_in_transp,geneids_out))
    pcl_out = handleNxMgenes(pcl_geneids_replaced, " /// ")
else:
    sys.stderr.write("+++ ERROR in GeneIDMapping +++ Mapping file does not exist. Return original file.\n")               
    pcl_out = pcl_in
                                                              
savePCLAsTxtFile (c_pcl_outputfile, pcl_out)

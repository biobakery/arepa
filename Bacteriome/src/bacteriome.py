#! /usr/bin/env python
import csv
import sys
import arepa
import sfle
import os
            

if len( sys.argv ) < 3:
    raise Exception( "Usage: bacteriome.py <inputfile.txt>  <output>" )
    
#Input Arguments:
c_inputfile = sys.argv[1]
c_resfile = sys.argv[2]


#Constants required for downloaded file: which ids are in which columns?
cols_keggnames = [0,2]
#cols_genenames = [1,3]
cols_score     = 4


#########################################################
# Local functions
#######################################################

#Reads complete table file into a list
def readTable(table):
    content = []
    f = csv.reader(open(table),delimiter="\t")
    [content.append(col) for col in f]
    return content


#Transpose a given matrix
def transpose(matrix):
    return [[matrix[x][y] for x in range(len(matrix))] for y in range(len(matrix[0]))]


#Saves a matrix as a file
def saveMatrixAsTxtFile (txtfile, content):
    with open(txtfile, 'w') as file:
        file.writelines('\t'.join(i) + '\n' for i in content)


#########################################################
# Main part
#######################################################

table_in = readTable(c_inputfile)
table_in_transp = transpose(table_in)
IntA_keggnames = table_in_transp[cols_keggnames[0]]
IntB_keggnames = table_in_transp[cols_keggnames[1]]
#IntA_genenames = table_in_transp[cols_genenames[0]]
#IntB_genenames = table_in_transp[cols_genenames[1]]
Int_scores     = table_in_transp[cols_score]

saveMatrixAsTxtFile(c_resfile, transpose([IntA_keggnames, IntB_keggnames, Int_scores]))




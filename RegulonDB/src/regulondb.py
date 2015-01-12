#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import csv
import sys
import arepa
import sfle
import os
			
if len( sys.argv ) < 3:
	raise Exception( "Usage: regulondb.py <inputfile.txt>  <outputfile.txt>" )
	
#Input Arguments:
c_inputfile = sys.argv[1]
c_resfile = sys.argv[2]


#Constants required for downloaded file: which ids are in which columns?
cols_genes = [0, 1]
cols_scores = 2


#======================================================
# Local functions
#======================================================

#Reads complete table file into a list
def readTableWithoutHeader(table):
	content = []
	f = csv.reader(open(table), delimiter="\t")
	for col in f:
		if col != []:
			if col[0]!='' and not col[0].startswith("#"):
				col[cols_scores]='1' #replace "-" or "+" with weigth "1"
				content.append(col)
	return content

#Transpose a given matrix
def transpose(matrix):
	return [[matrix[x][y] for x in range(len(matrix))] for y in range(len(matrix[0]))]

#Saves a matrix as a file
def saveMatrixAsTxtFile (txtfile, content):
	with open(txtfile, 'w') as file:
		file.writelines('\t'.join(i) + '\n' for i in content)

#======================================================
# Main  
#======================================================

table_in = readTableWithoutHeader(c_inputfile)
table_in_transp = transpose(table_in)
IntA  = table_in_transp[cols_genes[0]]
IntB = table_in_transp[cols_genes[1]]
#Write all gene ids as lower case for further mapping reasons:
IntAa = []
for ia in IntA:
	IntAa.append(ia.lower())
IntBb = []
for bi in IntB:
	IntBb.append(bi.lower())
Scores = table_in_transp[cols_scores]
saveMatrixAsTxtFile(c_resfile, transpose([IntAa, IntBb, Scores]))


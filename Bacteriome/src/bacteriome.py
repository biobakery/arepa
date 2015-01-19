#! /usr/bin/env python
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
	raise Exception( "Usage: bacteriome.py <inputfile.txt>  <output>" )
	
#Input Arguments:
c_inputfile = sys.argv[1]
c_resfile = sys.argv[2]

#Constants required for downloaded file: which ids are in which columns?
cols_keggnames = [0, 2]
cols_score	 = 4

#======================================================
# Local functions
#======================================================

#Reads complete table file into a list
def readTable(table):
	content = []
	f = csv.reader(open(table), delimiter="\t")
	[content.append(col) for col in f]
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

table_in 	= readTable(c_inputfile)
table_in_transp = transpose(table_in)
IntA_keggnames	= table_in_transp[cols_keggnames[0]]
IntB_keggnames	= table_in_transp[cols_keggnames[1]]
Int_scores	= table_in_transp[cols_score]

saveMatrixAsTxtFile(c_resfile, transpose([IntA_keggnames, IntB_keggnames, Int_scores]))

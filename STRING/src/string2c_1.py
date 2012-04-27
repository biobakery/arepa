#! /usr/bin/env python
import csv
import sys
import os
            


#Input Arguments:
inputfile = sys.argv[1]
outputfile = sys.argv[2]


# STRING specific constants:
c_IntA = "item_id_a"
c_IntB = "item_id_b"
c_Mode = "mode"
c_Score = "score"

pmid = "pmid:"
taxid = "taxid:"


def reorganizetable(inputfile):
    content = []
    myfileobj = open(inputfile, 'r')
    csv_read = csv.reader(myfileobj,dialect=csv.excel_tab)
    headerline = csv_read.next() #skip header line
    IntA = headerline.index(c_IntA)
    IntB = headerline.index(c_IntB)
    Mode = headerline.index(c_Mode)
    Score = headerline.index(c_Score)
    content = []#["#taxa_a\t#" + c_IntA + '\t#'+ "taxa_b\t#" + c_IntB + "\t#" + c_Mode + "\t#" +c_Score]
    for line in csv_read:
        try:
            txA, iA = line[IntA].split('.')
            txB, iB = line[IntB].split('.')
            md = pmid+line[Mode]
            sc = line[Score]
            content.append(iA+"\t"+iB+"\t"+taxid+txA+"\t"+taxid+txB+"\t"+md+"\t"+sc)
        except ValueError:
            continue
            #        content.append(taxid+line[IntA].replace('.','\t')+'\t'+taxid+line[IntB].replace('.','\t')+'\t'+pmid+line[Mode]+'\t'+line[Score])
    return content


def RemoveDubFromList(mylist):
    if mylist:
        mylist.sort()
        last = mylist[-1]
        for i in range(len(mylist)-2, -1, -1):
            a = "\t".join(mylist[i].split("\t")[0:5])
            b = "\t".join(last.split("\t")[0:5])
            if a == b:
                del mylist[i]
            else:
                last = mylist[i]
    return mylist



def removeDoubleEntries(array):
    vec = []
    for i in range(len(array)):
        vec.append("\t".join(array[i].split('\t')))
    vec2 = RemoveDubFromList(vec)
    return vec2





def saveMatrixAsTxtFile (txtfile, content):
    with open(txtfile, 'w') as file:
        #file.write("\n".join(content))
        file.writelines(i + '\n' for i in content)

    
table_in = reorganizetable(inputfile)
table_out = removeDoubleEntries(table_in)
saveMatrixAsTxtFile ( outputfile, table_out)

#!/usr/bin/env python

import csv
import pickle
import sys

hashData = pickle.load( sys.stdin )
csvw = csv.writer( sys.stdout, csv.excel_tab )
for strKey, pValue in hashData.items( ):
	csvw.writerow( (strKey, "%s" % pValue) )

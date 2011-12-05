import arepa 
import sys
import os 
import subprocess

def name_list(f_list = None, raw = None, dummylist = None):
	if not f_list:
		f_list = subprocess.check_output('ls')
		if not raw:
			raw = f_list.split('\n')
	if not dummylist:
		dummylist = []
	with open('names.txt', 'w') as outputf:
		for item in raw:
			if not ( item.startswith('GSE') or item.startswith('GDS') ):
				pass
			else: 
				outputf.write(str( item.split( '_' )[0] ))
				outputf.write('\n')
name_list()

	
		




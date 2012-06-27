import arepa
import random 
import types
import re  

# useful matrix functions 
def stripMat( m ):
        dummyMat = [] 
        for line in m:
                if isinstance(line, types.ListType):
                        dummyMat.append(map(lambda v: re.sub(r"[\t\n]","",v), line))
                else:
                        try:
                                dummyMat.append(re.sub(r"[\t\n]", "", str(line)))
                        except Exception:
                                pass 
        return dummyMat

def dict2mat( d, keyOrder = False ):
	''' 
	The value of the dictionary can be a list or a string. 
	Returns a tuple (mat, collist) where collist is the list of 
	the variable column lengths. If the key order pertinent, 
	pass in the keys in order to keyOrder.  
	'''
	new_matrix = [] 
	if keyOrder:
		dictKeys = keyOrder
	else:
		dictKeys = d.keys()
	for key in dictKeys:
		dummy = [key] 
		if type(d[key]) == list:
			for item in d[key]:
				dummy.append(item)
		else:
			try:
				dummy.append(str(d[key]))
			except Exception:
				continue  
		new_matrix.append( dummy )
	return new_matrix 

def maxlen( matrix ):
	iMax = 0 
	for row in matrix:
		if len(row) > iMax:
			iMax = len(row)
	return iMax 
 
def dict2colmat( d, keyOrder = False ):
	'''Takes a dictionary and produces 
	a matrix in which a column corresponds 
	to a vector of values for a specific label'''
	mat = dict2mat( d, keyOrder )
	maxcol = maxlen(mat) 
	new_mat = init(maxcol, len(mat), "")  
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			new_mat[j][i] = mat[i][j]
			print new_mat[j][i]
	return new_mat
	

import arepa
import random 
import types
import re  

# useful matrix functions 

def init(m,n,filler):
	new_matrix = [[filler for row in range(n)] for col in range(m)]
	return new_matrix 

def zero(m,n):
    # Create zero matrix
    return init(m,n,0)

def rand(m,n):
    # Create random matrix
    new_matrix = [[random.random() for row in range(n)] for col in range(m)]
    return new_matrix
 
def show(matrix):
    # Print out matrix
    for col in matrix:
        print col 
 
def mult(matrix1,matrix2):
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Dimensions do not match'
    else:
        # multiply if correct dimensions
        new_matrix = zero(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        return new_matrix
 
def add(matrix1, matrix2):
	# matrix addition 
	if (len(matrix1[0]) != len(matrix2[0])) | ( len(matrix1) != len(matrix2) ):
		print "Dimensions do not match"
	else:
		# add with correct dimensions	
		new_matrix = zero(len(matrix1),len(matrix1[0]))
		for i in range(len(matrix1)):
			for j in range(len(matrix1[0])):
				new_matrix[i][j] += matrix1[i][j] + matrix2[i][j]
	return new_matrix

def negate(matrix):
	new_matrix = zero(len(matrix),len(matrix[0]))
	for i in range(len(matrix)):
		for j in range(len(matrix[0])):
			new_matrix[i][j] = -1 * matrix[i][j]
	return new_matrix 

def transpose(matrix):
        new_matrix = zero(len(matrix[0]),len(matrix))
        for i in range(len(matrix)):
        	for j in range(len(matrix[0])):
			try:
                		new_matrix[j][i] = matrix[i][j]
			except IndexError:
				continue  
        return new_matrix

def c_mult(matrix, c):
        new_matrix = zero(len(matrix),len(matrix[0]))
        for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                        new_matrix[i][j] = c*matrix[i][j]
        return new_matrix

def column(matrix, n):
        return transpose([transpose(matrix)[n]])

def mean(matrix):
        new_matrix = zero(len(matrix), 1)           
        norm = 1.0/len(matrix[0])
        for i in range(len(matrix[0])):                 
                new_matrix = add(new_matrix,column(matrix,i))
        return c_mult(new_matrix,norm)

def covariance(matrix):
        m = mean(matrix)
        new_matrix = zero(len(matrix),len(matrix))
        for i in range(len(matrix[0])):
                xn = column(matrix,i)
                variance = add(xn, negate(m))
                new_matrix = add(mult(variance, transpose(variance)),new_matrix)
        return c_mult(new_matrix,(1.0/(len(matrix[0]))))                                         

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
	

import arepa

Import( "pE" )
Import( "afileSamples" )

c_strID					= arepa.dir( pE )
c_strDir				= c_strID + "/"
c_strFileIDTXT			= c_strDir + c_strID + ".txt"
c_strProgMergeTables	= "../../" + arepa.c_strSource + "merge_tables.py" 

pE.Dir( c_strDir )

arepa.cmd( pE, c_strProgMergeTables, c_strFileIDTXT,
	[[True, fileCur] for fileCur in afileSamples] )

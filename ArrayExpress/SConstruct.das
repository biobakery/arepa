import arepa

pE = Environment( )
c_strID					= arepa.dir( pE )
c_strFileIDTXT			= c_strID + ".txt"
c_strProgMergeTables	= arepa.path_arepa( ) + arepa.c_strSource + "merge_tables.py" 
c_astrInputsSamples		= Glob( "../*sample_table*" )

arepa.cmd( pE, c_strProgMergeTables, c_strFileIDTXT,
	[[True, fileCur] for fileCur in c_astrInputsSamples] )

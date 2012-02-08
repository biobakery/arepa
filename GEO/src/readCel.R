## Written by Levi Waldron on Feb 7, 2012
##
## Argument 1 is the name of the output file
## Argument 2 - end are the fully qualified paths of each CEL file
##
## This function reads the CEL files and writes an AffyBatch object to
## the output file.
##
## Sample input arguments:
##
## inputargs <- c("./testaffybatch.RData",dir("/my/celfile/directory/",pattern="\\.[cC][eE][lL]\\.[gG][zZ]$|\\.[cC][eE][lL]$",full.names=TRUE))

inputargs <- commandArgs(TRUE)

library(affy)

print(inputargs)
sessionInfo()


strOutputData		<- inputargs[1]
strInputCelfiles        <- inputargs[-1]

affybatch <- read.affybatch(filenames=strInputCelfiles)

save(affybatch,file=strOutputData,compress="bzip2")

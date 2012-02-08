## Written by Levi Waldron on Feb 7, 2012.
##
## Argument 1 is the name of the input file.  This is an R image file
## containing the object "affybatch" which is of class AffyBatch.
## 
## Argument 2 is the name out the output file.  It will be an R image
## file containing the object "eset" which is normally of class ExpressionSet.
##
## Argument 3 is the name of a preprocessing function, for example
## affy::rma (before double :: is the package name, after is the
## function name).
## 
## This function preprocesses raw data to produce normalized data.  It
## will usually be used for Affymetrix data, but should be equally
## applicable to other platforms, as long as the function provided by
## argument 3 can recognize and act on the input object "affybatch".
##
## Sample input arguments:
##
## inputargs <- c("./testaffybatch.RData","./testeset.RData","affy::rma")
## inputargs <- c("./testaffybatch.RData","./testeset.RData","affy::mas5")

inputargs <- commandArgs(TRUE)
print(inputargs)
sessionInfo()

strInputData		<- inputargs[1]
strOutputData		<- inputargs[2]
strProcessingFunction   <- inputargs[3]

strPackage <- strsplit(strProcessingFunction,split="::")[[1]][1]
library(strPackage,character.only=TRUE)

funPreprocess <- get(strsplit(strProcessingFunction,split="::")[[1]][2])

load(strInputData)

eset <- funPreprocess(affybatch)

save(eset,file=strOutputData,compress="bzip2")

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
## inputargs <- c("../data/GSE21815/GSE21815/GSE21815_01norm.pcl","./testeset.RData","affy::mas5")

inputargs <- commandArgs(TRUE)
print(inputargs)

strInputData		<- inputargs[1]
strOutputData		<- inputargs[2]
strProcessingFunction   <- inputargs[3]

strPackage <- strsplit(strProcessingFunction,split="::")[[1]][1]
library(affy)
library(strPackage,character.only=TRUE)

sessionInfo()

funPreprocess <- get(strsplit(strProcessingFunction,split="::")[[1]][2])

if(grepl("\\.RData$",strInputData)){
  ##input is an R object
  load(strInputData)
  eset <- funPreprocess(affybatch)
}

if(grepl("\\.pcl$",strInputData)){
  ##input is a pcl file
  mdExprs <- read.delim(strInputData,row.names=1)
  ##first row and first two columns are cruft
  mdExprs <- mdExprs[-1,-1:-2]
  mdExprs <- as.matrix(mdExprs)
  ##Get rid of anything past the GSM[0-9]+ in the column names
  colnames(mdExprs) <- gsub("(GSM[0-9]+)(.*)","\\1",colnames(mdExprs))
  ##log2 transformation if appropriate
  if( min( mdExprs, na.rm = TRUE ) >= 0 & max( mdExprs, na.rm = TRUE ) >= 50 ) {
    mdExprs <- log(mdExprs, base = 2)
  }
  ##make a fake AnnotatedDataFrame until we can load the real metadata.
  adf <- new("AnnotatedDataFrame",data=data.frame(sample=1:ncol(mdExprs),row.names=colnames(mdExprs)))
  ##Create the ExpressionSet
  eset <- new("ExpressionSet",
              exprs=mdExprs,
              phenoData=adf)
}

save(eset,file=strOutputData,compress="bzip2")

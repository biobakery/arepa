## ARepA: Automated Repository Acquisition 
## 
## ARepA is licensed under the MIT license.
## 
## Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
## files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
## use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
## to whom the Software is furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all copies or 
## substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
## INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
## IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
## WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
## OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Written by Levi Waldron on Feb 7, 2012.
## Updated by Levi Waldron on Jan 14, 2012 to populate the eset with
## MIAME information and platform annotation.
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
## No PMID:
## inputargs <- c("../data/GSE10183/GSE10183/GSE10183_01norm.pcl","./testeset.RData","affy::mas5", "../data/GSE10183/GSE10183/GSE10183_exp_metadata.txt","../data/GSE10183/GSE10183/GSE10183_cond_metadata.txt")
## Has PMID:
## inputargs <- c("../data/GSE18655/GSE18655/GSE18655_01norm.pcl","./testeset.RData","affy::mas5", "../data/GSE18655/GSE18655/GSE18655_exp_metadata.txt","../data/GSE18655/GSE18655/GSE18655_cond_metadata.txt")
## sub-platform:
## inputargs <- c("../data/GSE19829/GSE19829-GPL570/GSE19829-GPL570_01norm.pcl","./testeset.RData","affy::mas5", "../data/GSE19829/GSE19829-GPL570/GSE19829-GPL570_exp_metadata.txt","../data/GSE19829/GSE19829-GPL570/GSE19829-GPL570_cond_metadata.txt")
## GDS with sub-platform:
## inputargs <- c("../data/GDS2782/GDS2782-GPL570/GDS2782-GPL570_00raw.pcl", "../data/GDS2782/GDS2782-GPL570/GDS2782-GPL570.RData", "affy::rma", "../data/GDS2782/GDS2782-GPL570/GDS2782-GPL570_exp_metadata.txt")
## something
## inputargs <- c("../data/GSE10183/GSE10183/GSE10183_01norm.pcl","./testeset.RData","affy::mas5", "../data/GSE10183/GSE10183/GSE10183_exp_metadata.txt","../data/GSE10183/GSE10183/GSE10183_cond_metadata.txt")

inputargs <- commandArgs(TRUE)
print(inputargs)

strInputData		<- inputargs[1]
strOutputData		<- inputargs[2]
strProcessingFunction   <- inputargs[3]
##per-condition and per-experiment metadata:
strInputExperiment      <- inputargs[4]
strInputConditional     <- inputargs[5]

##Nothing is done with these yet, but these will be used to populate the ExpressionSet:
dfExperiment <- read.delim(strInputExperiment, as.is=TRUE)

##If dfExperiment has more than one platform, set it to the one being used here:
if( grepl("GPL[0-9]+ GPL[0-9]+", dfExperiment$platform) ){
    possible.platforms <- strsplit(dfExperiment$platform, split=" ")[[1]]
    this.platform <- strsplit(dirname(strInputExperiment), split="/")[[1]]
    this.platform <- this.platform[length(this.platform)]
    this.platform <- strsplit(this.platform, split="-")[[1]][2]
    dfExperiment$platform <- this.platform
}

strPackage <- strsplit(strProcessingFunction,split="::")[[1]][1]
library(affy)
library(strPackage,character.only=TRUE)

sessionInfo()


if(grepl("\\.RData$",strInputData)){
    ##input is an R object
    load(strInputData)
    funPreprocess <- get(strsplit(strProcessingFunction,split="::")[[1]][2])
    eset <- funPreprocess(affybatch)
    strProcessing.used <- strProcessingFunction
}else{
    strProcessing.used <- "default"
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
  ##Create the ExpressionSet
  eset <- new("ExpressionSet", exprs=mdExprs)
}

##Optional conditional metadata argument  
if( length( inputargs ) > 4 ){
    dfConditional <- read.delim(strInputConditional, as.is=TRUE, row.names=1)
}else{
    dfConditional <- data.frame(samplename=sampleNames(eset), row.names=sampleNames(eset), stringsAsFactors=FALSE)
    warning("per-condition metadata not available.")
}

adf <- new("AnnotatedDataFrame",data=dfConditional)

if( identical(sampleNames(adf), sampleNames(eset)) ){
    phenoData(eset) <- adf
}else{
    stop("Samples names did not match between eset and adf.")
}

##Decorate with experiment data
if( "pmid" %in% colnames(dfExperiment) & require(annotate)){
    print("Querying Pubmed...")
    experiment.miame <- pmid2MIAME(as.character(dfExperiment$pmid))
}else{
    experiment.miame <- new("MIAME")
    if (!is.null(dfExperiment$Series_contact_name))
        experiment.miame@name <- dfExperiment$Series_contact_name
    if(!is.null(dfExperiment$title))
        experiment.miame@title <- dfExperiment$title
    if(!is.null(dfExperiment$Series_contact_laboratory))
        experiment.miame@lab <- dfExperiment$Series_contact_laboratory
    if (!is.null(dfExperiment$Series_relation))
        experiment.miame@url <- sub("BioProject: ", "", dfExperiment$Series_relation)
    if(!is.null(dfExperiment$gloss))
        experiment.miame@abstract <- dfExperiment$gloss
}

if( require( GEOmetadb )){
    if (file.exists("../../../tmp/GEOmetadb.sqlite")){
        sqlfile <- "../../../tmp/GEOmetadb.sqlite"
    }else{
        dir.create("../../../tmp", showWarnings=FALSE)
        sqlfile = getSQLiteFile(destdir="../../../tmp")
    }
    con = dbConnect("SQLite",sqlfile)
    bioc.platform <- dbGetQuery(con,paste("select bioc_package from gpl where gpl='",dfExperiment$platform,"'", sep="") )[,1]
    if(is.na(bioc.platform))
        bioc.platform <- dfExperiment$platform
}else{
    bioc.platform <- dfExperiment$platform
}

experiment.miame@preprocessing <- list(strProcessing.used)
experiment.miame@other <- dfExperiment

##Now insert the experiment info into the eset:
experimentData(eset) <- experiment.miame
eset@annotation <- bioc.platform

save(eset,file=strOutputData,compress="bzip2")

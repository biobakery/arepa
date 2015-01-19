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


##R CMD BATCH --vanilla "--args GSE29221.RData GSE29221.Rd" esetToHelp.R
## Look here for an example of the directory structure (on hutlab4):
## /home/lwaldron/hg/curatedovariandata/curation/ovarian/curatedOvarianData
## ignore inst/ tests/ and CHANGELOG.  You need man/, data/, NAMESPACE (just copy),

## DESCRIPTION:
## Suggests: survival
## Don't need URL, biocViews, License

## Will also need an equivalent of man/curatedOvarianData-package.Rd.  Could be a template for now.

inputargs <- commandArgs(TRUE) 
print(inputargs)

file.in <- inputargs[1]
file.out <- inputargs[2]

library(affy)

##file.in <- "GDS104-GPL67.RData"
##file.out <- "GDS104-GPL67.Rd"

object.name <- sub(".Rd", "", file.out, fixed=TRUE)
object.name <- make.names(basename(object.name))
object.name <- paste(object.name, "_eset", sep="")

getEset <- function(file.in=file.in){
    library(affy)
    load(file.in)
    obj.classes <- sapply(ls(), function(x) class(get(x)))
    obj.wanted <- names(obj.classes)[obj.classes == "ExpressionSet"][1]
    get(obj.wanted)
}

##assign(object.name, getEset(file.in))
eset <- getEset(file.in)

pdata.nonblank <- pData(eset)
pdata.nonblank <- pdata.nonblank[,apply(pdata.nonblank,2,function(x) sum(!is.na(x)) > 0)]

sink(file=file.out)
writeLines( paste("\\title{", object.name, "}", sep="") )
writeLines( paste("\\name{", object.name, "}", sep="") )
writeLines( paste("\\alias{", object.name, "}", sep="") )
writeLines( "\\docType{data}")
writeLines( "" )

accessionID <- sub(".RData", "", file.in)

writeLines("\\description{")
writeLines(paste("assayData:", nrow(eset),"features,",ncol(eset),"samples"))
writeLines("")
writeLines(paste("First 6 feature names:", paste(head(featureNames(eset)), collapse=" ")))
writeLines("")
writeLines(paste("First 6 sample names:", paste(head(sampleNames(eset)), collapse=" ")))
writeLines("")
writeLines(paste("Annotation:", eset@annotation))
writeLines("")

writeLines( "--------------------------- ")
writeLines( "Study-level meta-data: ")
writeLines( "--------------------------- ")
writeLines("")

print( experimentData(eset) )

writeLines("")

writeLines( "--------------------------- ")
writeLines( "Sample-level meta-data: ")
writeLines( "--------------------------- ")
writeLines( "")
if (class(pdata.nonblank) == "data.frame"){
    for (iCol in 1:ncol(pdata.nonblank)){
        if(length(unique(pdata.nonblank[,iCol])) < 6)
            pdata.nonblank[,iCol] <- factor(pdata.nonblank[,iCol])
        writeLines(paste(colnames(pdata.nonblank)[iCol],": ",sep=""))
        print(summary(pdata.nonblank[,iCol]))
        writeLines("")
    }
}

writeLines("")
writeLines("}")
writeLines("")

sink(NULL)


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

library(affy)
if(!require(arrayQualityMetrics)){
    library(BiocInstaller)
    biocLite("arrayQualityMetrics")
    library(arrayQualityMetrics)
}

##inputargs <- c("GSE19831.RData","GSE19831_QC")
inputargs <- commandArgs(TRUE)
print(inputargs)
sessionInfo()

## The input file can be any of the following, in order of descending
## preference:
##
## 1. A file with .RData extension containing an AffyBatch object
## (best, because ArrayQualityMetrics gives the most information for
## this object class)
##
## 2. A file with .RData extension containing any of: ‘ExpressionSet’,
##          ‘NChannelSet’, ‘ExpressionSetIllumina’, ‘RGList’, ‘MAList’.
##
## 3. A text file with any other extension.  In ARepA this would most
## likely be a file ending in "_rdata.txt". The first column is
## assumed to contain feature names, and the first row is assumed to
## contain sample names.  The data.table::fread() command used
## attempts to auto-detect a number of attributes about the file, such
## as delimiter type.

file.in <- inputargs[1]  ## .RData file containing an AffyBatch object or ExpressionSet object, or a text file.
dir.out <- dirname(inputargs[2])  ## Directory path where output QC report will be put

origobj <- c(ls(), "origobj")

if(grepl("RData", file.in)){
    load(file.in)
    affyobj.name <- ls()[!ls() %in% origobj]
    assign(x="affyobj", value=get(affyobj.name))
}else{
    if(!require(data.table)){
        library(BiocInstaller)
        biocLite("data.table")
        library(data.table)
    }
    mdExprs <- fread(file.in)
    mdExprs <- data.frame(mdExprs)
    rownames(mdExprs) <- mdExprs[, 1]
    mdExprs <- as.matrix(mdExprs[, -1])
    affyobj <- new("ExpressionSet",exprs=mdExprs)
}

x <- arrayQualityMetrics(expressionset = affyobj,
                         outdir=dir.out,
                         force = TRUE,
                         spatial=FALSE)

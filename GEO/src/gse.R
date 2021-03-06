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


##inputargs <- c("/home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_series_matrix.txt.gz","/home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rplatform.txt","/home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rmetadata.txt","/home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rdata.txt")
##
## R CMD BATCH --vanilla "--args /home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_series_matrix.txt.gz /home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rplatform.txt /home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rmetadata.txt /home/lwaldron/hg/arepa/GEO/data/GSE7055-GPL4700/GSE7055-GPL4700/GSE7055-GPL4700_rdata.txt" gse.R &

library(GEOquery)
#options(download.file.method="wget")

inputargs <- commandArgs(TRUE)
print(inputargs)
sessionInfo()


##this will stay the same, but be step 2.  
strInputFile		<- inputargs[1]
strOutputPlatform	<- inputargs[2]
strOutputMetadata	<- inputargs[3]
strOutputData		<- inputargs[4]

##dirty hack to get just the GSE identifier from the data directory:
gsegpl <- strsplit(strInputFile,split="/")[[1]]
(gsegpl <- gsegpl[length(gsegpl)-1])

##get the destination directory:
targetdir <- strsplit(strOutputPlatform,split="/")[[1]]
targetdir <- targetdir[-length(targetdir)]
(targetdir <- paste(paste(targetdir,collapse="/"),"/",sep=""))

if(grepl("-",gsegpl)){  #if there is a "-"
  strInputAccession <- strsplit(gsegpl,"-")[[1]][1]
  strPlatform <- strsplit(gsegpl,"-")[[1]][2]
}else{
  strInputAccession <- gsegpl
}

if(all(sapply(inputargs,file.exists))){
  print("Files already exist, nothing left to do.")
  quit(save="no", status = 0)
}

if(file.exists(strInputFile)){  #get from disk
  print("Using previously downloading series matrix file.")
  gsedat <- getGEO(filename=strInputFile,destdir=targetdir,AnnotGPL=FALSE)
}else{  #get from GEO
  print("Downloading series matrix file(s) from GEO.")
  gsedat <- getGEO(strInputAccession,destdir=targetdir,AnnotGPL=FALSE)
}

if(class(gsedat) == "list" & length(gsedat) > 1){
    platforms.in.gse <- sapply(gsedat,function(x) x@annotation)
    if(exists("strPlatform"))
        gsedat <- gsedat[platforms.in.gse %in% strPlatform]
}

if(class(gsedat)=="list" & length(gsedat) > 1){  ##Try to merge multiple esets if they are from the same platform
  ##Write out merged series matrix file:
  series.matrix.files <- paste(targetdir,names(gsedat),sep="")
  series.matrix.list <- lapply(series.matrix.files,function(x) readLines(gzfile(x)))
  series.matrix.merged <- series.matrix.list[[1]]
  for (i in 2:length(series.matrix.list)){
    ##Growing a vector like this is fine for a short loop such as this.
    series.matrix.merged <- c(series.matrix.merged,
                              series.matrix.list[[i]][!grepl("^!Series",series.matrix.list[[i]])])
  }
  print("Writing merged series matrix file.")
  writeLines(series.matrix.merged,con=gzfile(strInputFile))
  rm(series.matrix.files,series.matrix.list,series.matrix.merged)
  ##Create merged R object
  exprs.cbind <- do.call(cbind,lapply(gsedat,exprs))
  pdata <- lapply(gsedat,pData)
  pdatMerge <- function(pdata.list){
    output.colnames <- unique(unlist(lapply(pdata.list,colnames)))
    pdata.matchedcols <- lapply(pdata.list,function(x){
      for (addcol in output.colnames[!output.colnames %in% colnames(x)]){
        x[[addcol]] <- NA
      }
      x <- x[,match(output.colnames,colnames(x))]
      return(x)
    }
                                )
    names(pdata.matchedcols) <- NULL  #necessary to maintain rownames in next line
    output <- do.call(rbind,pdata.matchedcols)
    return(output)
  }
  pdata.merged <- pdatMerge(pdata)
  ##if there are "." in rownames(pdat.merged
  pdata.merged <- pdata.merged[match(colnames(exprs.cbind),rownames(pdata.merged)),]
  if(identical(all.equal(rownames(pdata.merged),colnames(exprs.cbind)),TRUE)){
    gsedat <- new("ExpressionSet",
                  exprs=exprs.cbind,
                  phenoData=new("AnnotatedDataFrame",data=pdata.merged)
                  )
  }else{stop("Could not combine multiple ExpressionSets into one.")}
}

##Make sure gsedat is a list, because we will loop over the list for final processing:
if(class(gsedat)=="ExpressionSet"){
  gsedat <- list(gsedat)
  names(gsedat) <- paste(strInputAccession,"_series_matrix.txt.gz",sep="")
}

##One platform only
eset <- gsedat[[1]]
origpdat <- pData(eset)
write.csv(origpdat,file=strOutputMetadata)
mdExprs <- exprs(eset)
if( min( mdExprs, na.rm = TRUE ) >= 0 & max( mdExprs, na.rm = TRUE ) >= 50 ) {
  mdExprs <- log(mdExprs, base = 2)
  exprs(eset) <- mdExprs
}
write.csv(mdExprs,file=strOutputData)
## get platform info, ie annotation (GPL)
gpl <- unique(as.character(origpdat$platform_id))
gpldat <- getGEO(gpl,destdir=targetdir,AnnotGPL=FALSE)
gpltable <- Table(gpldat)
write.csv(gpltable,file=strOutputPlatform,row.names=FALSE)

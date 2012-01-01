##$REXEC CMD BATCH --vanilla "--args GSE12418 $DATAHOME" $SRCHOME/gse_PROCESSED.R $LOG/GSE8402_downloadPROCESSED.log
##inputargs <- c("GSE25220","../DATA")
##gds: GDS2785,GDS3297
##gse with no issues: GSE7463,GSE8842,GSE18520,GSE14764,GSE13525,GSE12470
##gse with issues: GSE19829,GSE9891,GSE13876

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
gsegpl <- gsegpl[length(gsegpl)-1]

if(grepl("-",gsegpl)){  #if there is a "-"
  strInputAccession <- strsplit(gsegpl,"-")[[1]][1]
  strPlatform <- strsplit(gsegpl,"-")[[1]][2]
}else{
  strInputAccession <- gsegpl
}

##strBaseDir <- inputargs[2]

if(!exists("strPlatform")){
  gsedat <- getGEO(strInputAccession)
}else{
  URLPrefix <- paste("ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SeriesMatrix/",strInputAccession,sep="")
  SeriesMatrixURL <- paste(URLPrefix,"/",gsegpl,"_series_matrix.txt.gz",sep="")
  download.file(SeriesMatrixURL,destfile=strInputFile)
  gsedat <- getGEO(filename=strInputFile)
}

if(class(gsedat)=="list" & length(gsedat) > 1){  ##Try to merge multiple esets if they are from the same platform
  platforms.in.gse <- sapply(gsedat,function(x) x@annotation)
  if(length(unique(platforms.in.gse))==1){
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
}

##Make sure gsedat is a list, because we will loop over the list for final processing:
if(class(gsedat)=="ExpressionSet"){
  gsedat <- list(gsedat)
  names(gsedat) <- paste(strInputAccession,"_series_matrix.txt.gz",sep="")
}

for (i in 1:length(gsedat)){
  dataset.name <- sub("_series_matrix.txt.gz","",names(gsedat)[i],fixed=TRUE)
  print(paste("Processing ",dataset.name,"...",sep=""))
  ##One platform only
  eset <- gsedat[[i]]   #if it's an ExpressionSet
  origpdat <- pData(eset)
  write.csv(origpdat,file=strOutputMetadata)
  mdExprs <- exprs(eset)
  if( min( mdExprs, na.rm = TRUE ) >= 0 & max( mdExprs, na.rm = TRUE ) >= 50 ) {
    mdExprs <- log(mdExprs, base = 2)
    exprs(eset) <- mdExprs
  }
  write.csv(mdExprs,file=strOutputData)
##  save(eset,file=paste(dataset.name,"_default_eset.RData",sep=""))
  ## get platform info, ie annotation (GPL)
  gpl <- unique(as.character(origpdat$platform_id))
  gpldat <- getGEO(gpl)
  gpltable <- Table(gpldat)
  write.csv(gpltable,file=strOutputPlatform,row.names=FALSE)
}

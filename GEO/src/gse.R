##nohup nice /shared/bin/R-2.11.1/bin/R CMD BATCH --no-save --no-restore '--args GSE12470' ~/arepa/GEO/src/getdefaultGRE.R output.log 2>&1 &

##gds: GDS2785,GDS3297
##gse with no issues: GSE7463,GSE8842,GSE18520,GSE14764,GSE13525,GSE12470
##gse with issues: GSE19829,GSE9891,GSE13876

library(GEOquery)
options(download.file.method="wget")

inputargs <- commandArgs(TRUE)
print(inputargs)
sessionInfo()

strInputFile		<- inputargs[1]
strOutputPlatform	<- inputargs[2]
strOutputMetadata	<- inputargs[3]
strOutputData		<- inputargs[4]

##dirty hack to get just the GSE identifier:
gse <- strsplit(strInputFile,split="/")[[1]]
gse <- gse[length(gse)-1]
gsedat <- getGEO(gse)
if(class(gsedat)=="list" & length(gsedat)==1) gsedat <- gsedat[[1]]

if(class(gsedat)=="list"){
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

if(class(gsedat)=="ExpressionSet"){
  ##One platform only
  eset <- gsedat   #if it's an ExpressionSet
  origpdat <- pData(eset)
  pdat <- pData(eset)[,grep("characteristics|title|source",colnames(pData(eset)))]  #broader
  write.csv(origpdat,file=strOutputMetadata)
#  write.table(pdat,sep="\t",file="default_pdata.txt")
	mdExprs <- exprs(eset)
	if( min( mdExprs, na.rm = TRUE ) >= 0 & max( mdExprs, na.rm = TRUE ) >= 50 ) {
		mdExprs <- log(mdExprs, base = 2) }
  write.csv(mdExprs,file=strOutputData)
#  save(eset,file="default_eset.RData")
  # get platform info, ie annotation (GPL)
  gpl <- unique(as.character(origpdat$platform_id))
  gpldat <- getGEO(gpl)
  gpltable <- Table(gpldat)
  write.csv(gpltable,file=strOutputPlatform,row.names=FALSE)
}else{
  stop(paste("gsedat was of class",class(gsedat)))
}

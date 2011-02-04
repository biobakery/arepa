##nohup nice /shared/bin/R-2.11.1/bin/R CMD BATCH --no-save --no-restore '--args GSE12470' ~/arepa/GEO/src/getdefaultGRE.R output.log 2>&1 &

##gds: GDS2785,GDS3297
##gse with no issues: GSE7463,GSE8842,GSE18520,GSE14764,GSE13525,GSE12470
##gse with issues: GSE19829,GSE9891,GSE13876

inputargs <- commandArgs(TRUE)
print(inputargs)
sessionInfo()

library(GEOquery)

if(length(grep("series_matrix",inputargs[1]))==1){
  ##this is a series, eg: "/home/lwaldron/GEO/GSE10952_series_matrix.txt.gz"
  seriesmatrix <- inputargs[1]
}else{  #then assume it's a GSE accesssion number
  gse <- inputargs[1]
  url <- paste("ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SeriesMatrix/",gse,"/",gse,"_series_matrix.txt.gz",sep="")
  system(paste("wget",url))
  seriesmatrix <- paste(inputargs[1],"_series_matrix.txt.gz",sep="")
}

gsedat <- getGEO(filename=seriesmatrix)

if(class(gsedat)=="ExpressionSet"){
  ##One platform only
  eset <- gsedat   #if it's an ExpressionSet
  origpdat <- pData(eset)
  pdat <- pData(eset)[,grep("characteristics|title|source",colnames(pData(eset)))]  #broader
  write.table(origpdat,sep="\t",file="full_pdata.txt")
  write.table(pdat,sep="\t",file="default_pdata.txt")
  write.csv(exprs(eset),file="default_exprs.csv")
  save(eset,file="default_eset.RData")
  # get platform info, ie annotation (GPL)
  gpl <- unique(as.character(origpdat$platform_id))
  gpldat <- getGEO(gpl)
  gpltable <- Table(gpldat)
  write.csv(gpltable,file="default_gpl.csv",row.names=FALSE)
}else{
  stop(paste("gsedat was of class",class(gsedat)))
}

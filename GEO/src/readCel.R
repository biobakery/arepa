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

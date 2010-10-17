#!/bin/sh
#
MSGFILE="/tmp/hgchgrp.txt";
DATESTAMP=`date "+%Y-%m-%d::%H:%M"`;

echo $DATESTAMP > $MSGFILE;
echo $PWD >> $MSGFILE;

hg -v tip >> $MSGFILE;
mail -s "Arepa: Hg Changegroup Received" hut-dev@hsphsun3.harvard.edu < $MSGFILE;
rm -f $MSGFILE

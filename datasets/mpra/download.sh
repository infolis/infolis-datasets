#!/bin/bash

pdfDir=pdf

while read metaFile;do
    id=$(basename $metaFile|sed 's/\.xml//')
    pdfFile="$pdfDir/$id.pdf"
    if [[ ! -e "$pdfFile" ]];then
        url=$(grep 'dc:identifier>http' $metaFile|grep -o 'http.*pdf')
        echo -n "Downloading for $id: $url ... "
        curl -s "$url" > $pdfFile
        echo "DONE"
        sleep 1
    fi
done < list


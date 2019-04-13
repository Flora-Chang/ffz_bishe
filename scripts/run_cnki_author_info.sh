#! /bin/bash

FILENAME='cnki.authors.part.1'
OUT_FILE='resources/done.cnki.authors.1.json'

cat ${FILENAME} | while read line
do
    scrapy crawl cnki_author_info -a url="${line}"
    echo ${line} >> ${OUT_FILE}
done
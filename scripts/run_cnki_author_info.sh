#! /bin/bash

FILENAME='line5.cnki.author.json'
OUT_FILE='resources/done.cnki.author_info.json'

cat ${FILENAME} | while read line
do
    scrapy crawl cnki_author_info -a url="${line}"
    echo ${line} >> ${OUT_FILE}
    break
done
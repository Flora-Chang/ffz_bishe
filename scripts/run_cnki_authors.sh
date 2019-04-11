#! /bin/bash

FILENAME='resources/pku_programs.json'
OUT_FILE='resources/done.pku_programs.json'

cat ${FILENAME} | while read line
do
    scrapy crawl cnki_authors -a row="${line}"
    echo ${line} >> ${OUT_FILE}
done
#! /bin/bash

FILENAME='data/cnki.authors.part.1'
OUT_FILE='resources/done.cnki.authors.1.json'

cat ${FILENAME} | while read line
do
    scrapy crawl cnki_author_info -a url="${line}"
    echo ${line} >> ${OUT_FILE}
done

# 修改内容
# 1. FILENAME
# 2. OUT_FILE
# 3. pipeline 内容
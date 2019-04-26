#! /bin/bash

IN_FILE='resources/authors_path/cnki.buzhua.author.cxc.'
OUT_FILE='resources/done.cnki.buzhua.authors.'

for (( i = 1; i <= 6; ++i )); do
    FILENAME=${IN_FILE}${i}
    cat ${FILENAME} | while read line
    do
        scrapy crawl cnki_author_info -a url="${line}"
        echo ${line} >> ${OUT_FILE}${i}
    done
done


# 修改内容
# 1. FILENAME
# 2. OUT_FILE
# 3. pipeline 内容

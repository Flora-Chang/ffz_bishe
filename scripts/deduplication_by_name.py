# -*- coding: utf-8 -*-
# @Time    : 2019/4/10 下午8:00
# @Author  : ffz@pku.edu.cn
# @version : 1.0
# @Site    : 
# @File    : deduplication_by_name.py
# @Breif   : 

from urllib import parse
import json
def deduplicate_by_name(src_file, dsc_file):
    name_set = set()
    cnt = 0
    with open(src_file, 'r') as src_f, open(dsc_file, "w") as dsc_f:
        for line in src_f:
            line = json.loads(line)
            url = line["url"]
            parsed_url = parse.urlparse(url)
            query_dict = parse.parse_qs(parsed_url.query)
            name = query_dict.get("skey", "")
            print(name)
            if name != "" and name[0] not in name_set:
                dsc_f.write(json.dumps(line, ensure_ascii=False)+"\n")
                name_set.add(name[0])
                cnt += 1
        print(cnt)



if __name__ == '__main__':
    deduplicate_by_name("/home/ffz/ffz_bishe/data/cnki.authors.uniq.json", "/home/ffz/ffz_bishe/data/cnki.authors.uniq.new.json")

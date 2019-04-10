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
    not_name_list = ["研究员", "教授", "副教授","博士", "博导", "编审", "对话人" , "演讲人", "对谈人" , "主持人", "主讲", "主讲人", "访谈", "整理人", "口述人", "数学家", "整理"]
    cnt = 0
    with open(src_file, 'r') as src_f, open(dsc_file, "w") as dsc_f:
        for line in src_f:
            line = json.loads(line)
            url = line["url"]
            parsed_url = parse.urlparse(url)
            # print(parsed_url)
            # print(parsed_url.query)
            query_dict = parse.parse_qs(parsed_url.query)
            # print(query_dict)
            name = query_dict.get("skey", [""])
            names = name[0].split()
            if len(names) > 1:
                name = ""
                tmp = "".join(names).lower().replace(" ", "").replace(".", "")
                flag = 0
                for c in tmp:
                    if c>'z' or c < 'a':
                        flag=1
                        break

                if flag == 1:
                    for word in names:
                        if len(word) >= 2 and len(word) <= 3 and word not in not_name_list:
                            name = word
                            break
                else:
                    name = " ".join(names)
            else:
                name = names[0]
            if name != "" and name not in name_set:
                print(names, name)
                query_dict['skey'] = [name]
                new_query = ""
                for key in query_dict:
                    new_query = new_query+ key+'='+query_dict[key][0]+'&'
                new_query = new_query[:-1]
                print(new_query)
                new_parsed_url = parse.ParseResult(scheme=parsed_url.scheme, netloc=parsed_url.netloc, path=parsed_url.path, params=parsed_url.params, query=new_query, fragment=parsed_url.fragment)
                new_url = parse.urlunparse(new_parsed_url)
                print(url)
                print(new_url)
                dsc_f.write(json.dumps({"url": new_url}, ensure_ascii=False)+"\n")
                name_set.add(name)
                cnt += 1
        print(cnt)



if __name__ == '__main__':
    deduplicate_by_name("/home/ffz/ffz_bishe/data/cnki.authors.uniq.json", "/home/ffz/ffz_bishe/data/cnki.authors.uniq.new.json")

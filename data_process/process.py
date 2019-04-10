# -*- coding: utf-8 -*-
# @Time    : 2018/11/9 下午4:57
# @Author  : ffz@pku.edu.cn
# @Site    : 
# @File    : process.py
# @Breif   : 数据处理相关脚本

import json
import time

def merge_programs(src_file, dsc_file):
    '''
    将programs.txt中一个老师的多个项目合并到一起，并以json形式返回
    :param src_file: 老师项目文件，txt格式，一行内容： 标号 \t 姓名 \t 项目名
    :param dsc_file: 老师项目文本，json格式，包含 "id":str, "name":str， "programs": list
    :return: None
    '''
    with open(src_file, "r", encoding="utf-8") as src_f, open(dsc_file, "w", encoding="utf-8") as dsc_f:
        id = None
        program_dict = {}
        cnt = 0
        for line in src_f:
            line = line.strip().split("\t")
            if len(line) < 3:
                continue
            if line[0].strip() == line[1].strip() or  len(line[2].strip().replace("*", ""))<=4 or line[1].strip()=="":
                # print(line)
                continue
            if id == None or id != line[0].strip():
                #print(line)
                if id != None:
                    cnt += 1
                    dsc_f.write(json.dumps(program_dict, ensure_ascii=False) + "\n")
                id = line[0].strip()
                name = line[1].strip().replace(" ", "")
                program = line[2].strip()
                program_dict["id"] = id
                program_dict["name"] = name
                program_dict["program"] = [program]
            elif id == line[0].strip():
                program_dict["program"].append(line[2].strip())
                print(line)
        print("{} teachers in all!".format(cnt))


def add_content_for_teacher_program(zhiwang_wanfang_data_file, src_file, dsc_file):
    '''
    利用从知网，万方这两大数据库中抓取的数据，扩充老师的基金，项目等信息
    :param zhiwang_wanfang_data_file: 知网，万方论文数据
    :param src_file: 老师项目标题
    :param dsc_file: 老师项目标题+摘要+关键字
    :return: 
    '''
    zhiwang_wanfang = open(zhiwang_wanfang_data_file, "r").readlines()
    src_f = open(src_file, "r")
    dsc_f = open(dsc_file, "w")
    cnt = 0
    for i, teacher_line in enumerate(src_f.readlines()):
        print(teacher_line)
        teacher_line = json.loads(teacher_line)
        teacher_line["zhiwang_wanfang"] = []
        name = teacher_line["name"].strip().replace(" ", "")
        for j, article_line in enumerate(zhiwang_wanfang):
            article_line = json.loads(article_line)
            authors = [_.strip().replace(" ", "") for _ in article_line.get("authors", [])]
            zuozhedanwei  = article_line.get("zuozhedanwei", "")
            if name in authors and "北京大学" in zuozhedanwei:
            # if name in authors:
                teacher_line["zhiwang_wanfang"].append(article_line)

        if teacher_line["zhiwang_wanfang"] != []:
            cnt += 1
            print(i)
            dsc_f.write(json.dumps(teacher_line, ensure_ascii=False) + "\n")
    print("find {} teachers have article!".format(cnt))





if __name__ == "__main__":
    # merge_programs("./programs.head35000.txt", "./programs.json")
    add_content_for_teacher_program("../ikreai/data/chinese/train.json", "./programs.json", "./programs_zhihu_wanfang.json")




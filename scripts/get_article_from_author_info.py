# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 下午8:51
# @Author  : ffz@pku.edu.cn
# @version : 1.0
# @Site    : 
# @File    : get_article_from_author_info.py
# @Breif   : 

import json, os, re
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from urllib import parse


def get_article_from_author_info(author_file, article_file):
    '''从原始作者信息中获取发表文章的url'''
    cnt = 0
    with open(author_file, 'r') as author_f, open(article_file, 'w') as article_f:
        article_set = set()
        for line in author_f:
            cnt += 1
            line = json.loads(line)
            articles = []
            articles.extend([x[0].replace("/kcms/detail//kcms/detail/", "/kcms/detail/") for x in line.get("zuigao_beiyin",[])])
            articles.extend([x[0].replace("/kcms/detail//kcms/detail/", "/kcms/detail/") for x in line.get("zuigao_xiazai",[])])
            articles.extend([x[0].replace("/kcms/detail//kcms/detail/", "/kcms/detail/") for x in line.get("qikan",[])])
            articles.extend([x[0].replace("/kcms/detail//kcms/detail/", "/kcms/detail/") for x in line.get("waiwen_qikan",[])])
            articles.extend([x[0].replace("/kcms/detail//kcms/detail/", "/kcms/detail/") for x in line.get("ceng_cankao",[])])
            for article in set(articles):
                if article not in article_set:
                    article_set.add(article)
                    if cnt > 4557:
                        article_f.write(article+"\n")

def get_author_from_author_info(author_file, author_url_file, new_author_file):
    '''从原始作者信息中获取合作者的url'''
    author_set = set()
    with open(author_url_file) as f:
        for line in f:
            line = json.loads(line)
            author_set.add(parse_url(line['url'], 'skey')[0].replace(" ", ""))
    with open(author_file, 'r') as author_f, open(new_author_file, 'w') as new_author_f:
        for line in author_f:
            line = json.loads(line)
            authors = []
            authors.extend(x for x in line.get("same_org_collaborator", [])[:3])
            authors.extend(x for x in line.get("other_org_collaborator", [])[:3])
            for author in authors:
                if author[0].replace(" ", "") not in author_set:
                    author_set.add(author[0])
                    new_author_f.write(json.dumps({"url": author[2],
                                        "name": author[0].replace(" ", ""),
                                        "code": author[1]}, ensure_ascii=False) +'\n')

def get_article_distribution_from_author_info(author_file):
    '''从原始作者信息中获取发表文章以及被引次数的分布， 以及合作者数量的分布'''
    with open(author_file, 'r') as author_f:
        pub_num_list = []
        download_num_list = []
        collaborator_num_list = []
        author_set = set()
        for line in author_f:
            line = json.loads(line)
            author_name = line['name'][0]
            if author_name in author_set:
                continue
            author_set.add(author_name)
            pub_num = line["pub_num"]
            download_num = line["download_num"]
            collaborator_num = len(line.get("same_org_collaborator", []) + line.get("other_org_collaborator", []))
            if pub_num > 2:
                pub_num_list.append(min(100, pub_num))
            download_num_list.append(download_num)
            collaborator_num_list.append(collaborator_num)
            # print(author_name, "pub_num: ", pub_num, "download_num: ", download_num, "collaborator_num: ", collaborator_num )
        return pub_num_list, download_num_list, collaborator_num_list

def parse_url(url, keyword):
    url_ = parse.urlparse(url)
    query_dict = parse.parse_qs(url_.query)
    value = query_dict.get(keyword, "")
    return value

def get_article_detail_distribution_from_article_info(article_file):
    '''从文章信息中获取摘要长度，标题长度，关键字个数，以及参考文献个数信息'''
    with open(article_file, 'r') as article_f:
        abstract_len_list = []
        keywords_num_list = []
        reference_num_list = []
        year_list = []
        title_len_list = []
        article_set = set()
        year_pattern = re.compile(r'\d+')
        for line in article_f:
            line = json.loads(line)
            filename = parse_url(line['url'], "filename")[0]
            dbname = parse_url(line['url'], "dbname")[0]
            year_match_dbname = year_pattern.search(dbname)
            year_match_filename = year_pattern.search(filename)
            if year_match_dbname:
                span = year_match_dbname.span()
                year = int(dbname[span[0]: span[0]+4])
            elif year_match_filename:
                span = year_match_filename.span()
                year = int(filename[span[0]: span[0] + 4])
            else:
                year = None
                print(line['url'])
            if filename not in article_set:
                article_set.add(filename)
                abstract = line["abstract"]
                title = line["title"]
                keywords = line["keywords"]
                references = line["references"]
                if abstract:
                    abstract_len_list.append(min(len(abstract), 1000))
                if title:
                    title_len_list.append(min(len(title), 100))
                if keywords:
                    keywords_num_list.append(min(len(keywords), 10))
                if references:
                    reference_num_list.append(min(len(references)+1, 24))
                if year>2000:
                    year_list.append(year)


        return {"abstract_len_list": abstract_len_list,
                "title_len_list": title_len_list,
                "keywords_num_list": keywords_num_list,
                "reference_num_list": reference_num_list,
                "year_list": year_list}




def plot_figure(num_list, xlabel, ylabel, title, ):
    num_bins = 20
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 23
             }

    count = np.array(num_list)
    # plt.hist(count)
    print(len(num_list))
    n, bins, patches = plt.hist(count, num_bins, facecolor='g', edgecolor="green", alpha=1.0, histtype='step', normed=1)
    # plt.figure(figsize=(8, 4))
    # plt.yticks([x for x in np.arange(0.0, 0.50,  0.02)])
    # plt.xticks([x for x in range(0, 105, 10)])
    # plt.yticks([x for x in np.arange(0.0, 0.50, 0.02)])
    # plt.xticks([x for x in range(0, 1000, 100)])
    # plt.yticks([x for x in np.arange(0.0, 0.50, 0.05)])
    plt.xticks([x for x in range(0, 12, 1)])
    # plt.yticks([x for x in np.arange(0.0, 0.50, 0.05)])
    # plt.xticks([x for x in range(0, 24, 1)])
    # plt.xticks([x for x in range(2000, 2020, 1)])
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)

    # plt.plot(bins[:-1], n / (0.1 + len(count)), 'g', label="摘要长度分布")
    # rects1 = plt.bar(left=x, height=num_list1, width=0.4, alpha=0.8, color='red', label="一部门")
    font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc', size=8)
    plt.xlabel(xlabel, fontproperties=font)
    plt.ylabel(ylabel, fontproperties=font)
    plt.title(title, fontproperties=font)
    plt.show()




if __name__ == '__main__':
    ROOT_PATH = "/root/ffz_bishe/information/resources/cnki_articles"
    # ROOT_PATH = "/Users/ffz/Documents/ffz_bishe/information/resources/cnki_articles"
    get_article_from_author_info(os.path.join(ROOT_PATH, "cnki.author_info.b.2.json"), os.path.join(ROOT_PATH, "cnki.buzhua.2.txt"))
    # get_author_from_author_info(os.path.join(ROOT_PATH, "cnki.author_info.b.2.json"), os.path.join(ROOT_PATH, "cnki.authors.uniq.new.json"), os.path.join(ROOT_PATH, "cnki.buzhua.author.2"))
    # pub_num_list, download_num_list, collaborator_num_list = get_article_distribution_from_author_info(os.path.join(ROOT_PATH, "cnki.author_info.b.json"))
    # plot_figure(pub_num_list, xlabel="Article Quantity", ylabel="Proportion", title="Article Quantity Distribution" )
    # ans_dict = get_article_detail_distribution_from_article_info(os.path.join(ROOT_PATH, "cnki.buzhua.1.json"))
    # plot_figure(ans_dict["abstract_len_list"], xlabel="Abstract Length", ylabel="Proportion", title="Abstract Length Distribution")
    # plot_figure(ans_dict["title_len_list"], xlabel="Title Length", ylabel="Proportion", title="Title Length Distribution")
    # plot_figure(ans_dict["keywords_num_list"], xlabel="关键词个数", ylabel="频率", title="关键词个数分布")
    # plot_figure(ans_dict["reference_num_list"], xlabel="参考文献数量", ylabel="频率", title="参考文献数量分布")
    # plot_figure(ans_dict["year_list"], xlabel="年份", ylabel="频率", title="年份分布")
# 新建爬虫
scrapy genspider cnki_new_spider "cnki.net"

# 知网数据
1. 根据作者和单位抓取的文章：cnki.*.json
2. 引用、读者推荐：cnki.cite.*.json
3. 随机文章：cnki.random.json

# 根据关键词抓取知网文章
1. 修改 cnki_random.py 中第45行的 cookie 信息
2. 运行 scrapy crawl cnki_random 命令，根据关键词随机抓取文章

cnki.author_info.1.json 文件里是文章url拼接有问题的，需要特殊处理
cnki.author_info.a.json 文件前3423行的waiwen_qikan 的 url 中间有 \n和空格，后续需要特殊处理
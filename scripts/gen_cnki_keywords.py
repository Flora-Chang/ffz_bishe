import json

# 1. 拿到所有引用和读者推荐内容，并且去掉已经抓到的
in_file = "../data/cnki.full.json"
out_file = "../tmp_data/cnki.keywords.txt"

keywords = set()


with open(in_file) as f, open(out_file, 'w') as fout:
    for line in f:
        item = json.loads(line.strip())

        for word in item.get('keywords'):
            if len(word.strip()) > 0:
                keywords.add(word.strip())

    for word in keywords:
        fout.write(word + "\n")


print("Done.")

import json

# 1. 拿到所有引用和读者推荐内容，并且去掉已经抓到的
in_file = "../data/cnki.full.json"
out_file = "../tmp_data/cnki.buzhua.txt"

ready_papers = set()
refs_recs_sims = set()


with open(in_file) as f, open(out_file, 'w') as fout:
    for line in f:
        item = json.loads(line.strip())
        ready_papers.add(item.get('url'))
        refs = item.get('references')
        recs = item.get("reader_recs")
        sims = item.get("similar_liters")

        for p in refs + recs + sims:
            refs_recs_sims.add(p[1])

    for url in refs_recs_sims - ready_papers:
        fout.write(url + "\n")


print("Done.")

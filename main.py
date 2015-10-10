__author__ = 'jiacheng'
#!/usr/bin/env python3
# -*- coding: utf-8 -*
import urllib.request as http
import json
from pics import picss
k = 0
s = ""
z = 0
for m in range(1, 11):
    html1 = "http://www.pixiv.net/ranking.php?mode=daily&content=illust&p="
    html2 = str(m)
    html3 = "&format=json&tt=50e0858285c8cab554d9622d092cbc25"
    html = html1+html2+html3
    jsons = http.urlopen(html).read().decode()
    jsons = json.loads(jsons)
    for i in jsons['contents']:
        k += 1
        if i["yes_rank"] == 0:
            z += 1
            s += '第%d:%d\n' % (k, i['illust_id'])
            print(k, i['illust_id'],  "请您耐心等待")
            picss(i['illust_id'])
            print('Complete')
with open("今日首次上榜.txt", 'w+') as f:
    f.write(s)

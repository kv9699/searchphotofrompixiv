__author__ = 'jiacheng'
#!/usr/bin/env python3
# -*- coding: utf-8 -*
import re
import urllib
from urllib import request
from download import down



def apics(p_id):
    req = request.Request('http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % p_id)
    s = request.urlopen(req).read().decode()
    re_p = r'(\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2}/)'
    if re.search(re_p, s):
        m = re.search(re_p, s)
        print(m.group())
    else:
        print("failed")
    for i in range(1, 5):
        url_p = "http://i%d.pixiv.net/img-original/img/%s%s_p0.png" % (i, m.group(), p_id)
        if not down(url_p):
            url_p = "http://i%d.pixiv.net/img-original/img/%s%s_p0.jpg" % (i, m.group(), p_id)
            down(url_p)
        else:
            break

if __name__ == '__main__':
    apics("52113838")




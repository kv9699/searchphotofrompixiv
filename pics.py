__author__ = 'jiacheng'
#!/usr/bin/env python3
# -*- coding: utf-8 -*
from urllib import request
import urllib
import re
from apic import apics
from download import down


def picss(pid):
    try:
        req = request.Request('http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % pid)
        reqs = request.Request('http://www.pixiv.net/member_illust.php?mode=manga&illust_id=%s' % pid)
        ss = request.urlopen(reqs).read().decode()
        s = request.urlopen(req).read().decode()
        re_p = r'(\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2}/)'
        if re.search(re_p, s):
            m = re.search(re_p, s)
            time = m.group()
        else:
            print("failed")
        for k in range(0, 5):
            for i in range(1, 5):
                url_p = "http://i%d.pixiv.net/img-original/img/%s%s_p%s.png" % (i, m.group(), pid, k)
                if not down(url_p):
                    url_p = "http://i%d.pixiv.net/img-original/img/%s%s_p%s.jpg" % (i, m.group(), pid, k)
                    down(url_p)
                else:
                    break
    except urllib.error.HTTPError as e:
        apics(pid)
    finally:
        pass



if __name__ == '__main__':
    picss("52113838")
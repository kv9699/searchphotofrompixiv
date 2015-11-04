__author__ = 'jiacheng'
# !/usr/bin/env python3
# -*- coding: utf-8 -*
from urllib import request
import urllib.parse
from pixivpy3api import *
import os
import re
from datetime import datetime
import _thread as thread, queue,time

stdoutmutex = thread.allocate_lock()
numconsumers = 5
numproducers = 4


class Search(object):

    def __init__(self, username, password):
        self.__list = []
        self.__api = PixivAPI()
        self.__api.login(username, password)
        self.mulu = os.path.join(os.path.abspath('.'), self.nows())
        if not [x for x in os.listdir('.') if os.path.isdir(x)].count(self.nows()):
            os.mkdir(self.mulu)

    def search_id(self, num=10):
        Q =self.__api.ranking_all(page=1)
        lens = len(Q["response"][0]['works'])
        if lens < num:
            num = lens
        j = 0
        while num > 0:
            j += 1
            if Q["response"][0]['works'][j]["previous_rank"] == 0:
                self.__list.append(Q["response"][0]['works'][j]['work']['id'])
                num -= 1
        return self.__list

    def find_url(self, id):
        urls = []
        l = JsonDict(self.__api.works(id))
        if l.response[0]['metadata']==None:
            url = l.response[0]['image_urls']['large']
            urls.append(url)
        else:
            for i in range(0, len(l.response[0]['metadata']['pages'])):
                url = l.response[0]['metadata']['pages'][i]["image_urls"]["large"]
                urls.append(url)
        return urls

    def downloads(self, url):
        iid, fwq, p0, hz = self.Extension(url)
        try:
            req = request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')
            #req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            #req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
            #req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
            #req.add_header('Connection', 'keep-alive')
            #req.add_header('Cookie', 'p_ab_id=1; __gads=ID=8198fd20deb760d6:T=1438656214:S=ALNI_MYMJP52ZiSlx1cVh9jOiQyoeT8kTQ; device_token=d2ed922273524949387b0ab1b649eb99; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; PHPSESSID=6767057_490d27cf4da1ff374c5429e96c9fee43; __utma=235335808.56850771.1438656214.1440306314.1440314248.5; __utmb=235335808.10.10.1440314248; __utmc=235335808; __utmz=235335808.1438656214.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=6767057=1; _ga=GA1.2.56850771.1438656214')
            req.add_header('DNT', '1')
            req.add_header('Referer', 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % id)
            req.add_header('Host', fwq)
            wenjian = '%s_p%s.%s' % (iid, p0, hz)
            path = os.path.join(self.mulu, wenjian)
            with open(path, 'wb') as f:
                f.write(request.urlopen(req).read())
        except urllib.error.HTTPError as e:
            print("error:%s" %e)


    def nows(self):
        now = str(datetime.now())
        time = r'(\d+)(\-)(\d+)(\-)(\d+)'
        m = re.search(time, now)
        return m.group()

    def Extension(self, url):
        re_s = r'(http://)([0-9a-zA-Z\.]*)/([0-9a-zA-Z\.\-]*)(/img/)' \
               r'(\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2}/)(\d*)(_p)(\d{1,2})(.)(\w\w\w)'
        if re.search(re_s, url):
            m = re.search(re_s, url)
            iid = m.group(6)
            fwq = m.group(2)
            p0 = m.group(8)
            hz = m.group(10)
        else:
            print("failed")
        return iid, fwq, p0, hz

dataQueue = queue.Queue()

def runss(username, password):
    k = Search(username, password)
    list = []
    for i in k.search_id():
        for j in k.find_url(i):
            list.append(j)
    global th_time
    th_time = len(list)
    thread.start_new_thread(producer, (list,))
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (k,))
    while True:
        if th_time == 0:
            break
    time.sleep(5)
    return True

def producer(list):
    for url in list:
        dataQueue.put(url)

def consumer(k):
    global th_time
    while True:
        try:
            url = dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            stdoutmutex.acquire()
            th_time -= 1
            stdoutmutex.release()
            k.downloads(url)

if __name__ == '__main__':
    k = Search('1111', "11111")
    urls = k.find_url(53273389)
    for url in urls:
        k.downloads(url)

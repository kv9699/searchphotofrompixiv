__author__ = 'jiacheng'
# !/usr/bin/env python3
# -*- coding: utf-8 -*
import json
import requests


class PixivError(Exception):  # Error class
    def __init__(self, reson):
        self.reson = reson
        Exception.__init__(self, reson)

    def __str__(self):
        return self.reson

    __repr__ = __str__


class JsonDict(dict):  # json dict
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise ArithmeticError(r"'JsonDict' object has no attribute '%s'" % item)

    def __setattr__(self, key, value):
        self[key] = value


class BasePixivAPi(object):
    def __init__(self):
        self.access_token = None  # initialization
        self.user_id = 0

    def pares_jason(self, json_str):  # json dict to python object
        def _obj_hook(pairs):
            o = JsonDict()
            for i, j in pairs.items():
                o[str(i)] = j
            return o
        return json.loads(json_str, object_hook=_obj_hook)

    def require_auth(self):  # check token
        if self.access_token == None:
            raise PixivError('Authentication required! Call login() or set_auth() first!')

    def requests_call(self, url, method="GET", headers={}, data=None, params={}):  # get & post
        self.req_header = {
            'Referer': 'http://spapi.pixiv.net',
            'User_Agent': 'pixivIOSApp/5.8.0',
        }
        for k,v in headers.items():   # write hander
            self.req_header[k] = v
        try:
            if method.upper() == 'GET':
                return requests.get(url, params=params, headers=self.req_header)
            elif method.upper() == 'POST':
                return requests.post(url, params=params, data=data, headers=self.req_header)
        except Exception as e:
            raise PixivError('requests %s %s error:%s' % (method, url, e))

    def set_auth(self, access_token):  # set up token
        self.access_token = access_token

    def login(self, username, password):
        url = 'https://oauth.secure.pixiv.net/auth/token'
        headers = {
            'Referer': 'http://www.pixiv.net',
        }
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
            'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
        }

        r = self.requests_call(url, method='post', headers=headers, data=data)  # use post
        if not (r.status_code in [200, 301, 302]):
            raise PixivError('[ERROR] login() failed! check username and '
                             'password.\nHTTP %s: %s' % (r.status_code, r.text))
        token = None
        try:
            token = self.pares_jason(r.text)  # jason token to str
            self.access_token = token.response.access_token
            self.user_id = token.response.user.id
            # print('AccessToken', self.access_token)
        except:
            raise PixivError('Get access_token error! Response: %s' % token)
        return token


class PixivAPI(BasePixivAPi):

    def auth_requests_call(self, url, method='GET', headers={}, data=None, params=None):
        self.require_auth()
        headers['Authorization'] = "Bearer %s" % self.access_token
        return self.requests_call(url, method=method, headers=headers, data=data, params=params)

    def pares_result(self, req):
        try:
            return self.pares_jason(req.text)
        except Exception as e:
            raise PixivError("parse_json() error: %s" % e)

    def bad_words(self):
        pass

    def works(self, illust_id):
        url = 'https://public-api.secure.pixiv.net/v1/works/%d.json' % illust_id
        params = {
            'profile_image_sizes': 'px_170x170,px_50x50',
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 'true',
        }
        r = self.auth_requests_call(url, params=params)
        return self.pares_result(r)

    def ranking_all(self, mode='daily', page=1, per_page=50, date=None, content='illust', image_sizes=['px_128x128', 'px_480mw', 'large'], profile_image_sizes=['px_170x170', 'px_50x50'], include_stats=True, include_sanity_level=True):
        url = 'https://public-api.secure.pixiv.net/v1/ranking/illust'
        params = {
            'mode': mode,
            'page': page,
           # 'content': content,
            'per_page': per_page,
            'include_stats': include_stats,
            'include_sanity_level': include_sanity_level,
            'image_sizes': ','.join(image_sizes),
            'profile_image_sizes': ','.join(profile_image_sizes),
        }
        if date:
            params['date'] = date
        r = self.auth_requests_call(url, params=params)
        return self.pares_result(r)

if __name__ == '__main__':
    k = PixivAPI()
    k.login("1111", "1111")
    Q =k.ranking_all()
    lens = len(Q["response"][0]['works'])
    i = 0
    j = 0
    while i < 10:
        j += 1
        if Q["response"][0]['works'][j]["previous_rank"] == 0:
            print(Q["response"][0]['works'][j]['work']['id'])
            i += 1

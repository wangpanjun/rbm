# -*- coding: utf-8 -*-
import json

from flask import render_template
from rbm import settings
import math

MIN_NUM = -2 << 64
MAX_NUM = 2 << 64


class RBMPagination(object):

    def __init__(self, page, page_size, total):
        self.page = page
        self.page_size = page_size
        self._total = total

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def pages(self):
        return math.ceil(self.total / self.page_size) if self.page_size > 0 else 1

    def show_pages(self):
        if self.page_size < 0:
            return [1]
        total_page = self.pages
        if total_page <= 5:
            return [i for i in range(total_page + 1) if i > 0]

        if self.page <= 3:
            return [i for i in range(6) if i > 0]

        if total_page - self.page <= 2:
            return [i for i in range(total_page - 5, total_page + 1)]

        return [i for i in range(self.page - 2, self.page + 3)]

    @property
    def tail(self):
        return self.pages


class RedisValues(object):

    @classmethod
    def get_ttl(cls, key):
        return settings.redis_conn.ttl(key)

    @classmethod
    def string_get(cls, key, payload=None):
        data = settings.redis_conn.get(key)
        data = data.decode('utf8') if data else data
        ttl = cls.get_ttl(key)
        return render_template("values/string.html", typ='string', key=key, data=data, ttl=ttl)

    @classmethod
    def list_get(cls, key, payload=None):
        page, page_size = 1, 10
        if payload:
            try:
                page = int(payload.get('page', 1))
            except ValueError:
                pass
            try:
                page_size = int(payload.get('page_size', 10))
            except ValueError:
                pass
        c = settings.redis_conn.llen(key)
        if page_size > 0:
            data = settings.redis_conn.lrange(key, (page - 1) * page_size, page * page_size)
        else:
            data = settings.redis_conn.lrange(key, 0, -1)

        page = RBMPagination(page, page_size, c)

        res = []
        for i in data:
            i = i.decode('utf8')
            try:
                i = json.loads(i)
            except ValueError:
                pass
            res.append(i)
        ttl = cls.get_ttl(key)
        return render_template("values/list.html", typ='list', key=key, data=json.dumps(res), c=c,
                               ttl=ttl, page=page)

    @classmethod
    def hash_get(cls, key, payload=None):
        data = settings.redis_conn.hgetall(key)
        dic = {}
        for k, v in data.items():
            v = v.decode('utf8')
            try:
                v = json.loads(v)
            except ValueError:
                pass
            dic.setdefault(k.decode('utf8'), v)
        data = json.dumps(dic)
        ttl = cls.get_ttl(key)
        return render_template("values/hash.html", typ='hash', key=key, data=data, ttl=ttl)

    @classmethod
    def zset_get(cls, key, payload=None):
        data = settings.redis_conn.zrange(key, 0, -1, withscores=True)
        c = settings.redis_conn.zcount(key, MIN_NUM, MAX_NUM)
        dic = {}
        for obj in data:
            dic[obj[0].decode('utf8')] = obj[1]
        ttl = cls.get_ttl(key)
        return render_template("values/zset.html", typ='zset', key=key, data=json.dumps(dic), c=c,
                               ttl=ttl)

    @classmethod
    def set_get(cls, key, payload=None):
        data = settings.redis_conn.smembers(key)
        ls = []
        for o in data:
            ls.append(o.decode('utf8'))
        c = len(data)
        ttl = cls.get_ttl(key)
        return render_template("values/set.html", typ='set', key=key, data=json.dumps(ls), c=c,
                               ttl=ttl)


if __name__ == '__main__':
    rbm = RBMPagination(11, 10, 101)
    print(rbm.show_pages())

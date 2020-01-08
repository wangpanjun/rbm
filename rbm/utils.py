# -*- coding: utf-8 -*-
import redis
import os

from rbm import settings
from rbm.settings import PROJECT_ROOT
from rbm.models import SettingsModel
from rbm.app import db

config_path = os.path.join(PROJECT_ROOT, 'settings.ini')

MIN_NUM = -2 << 64
MAX_NUM = 2 << 64


def change_redis_conn(s=None):
    if s:
        try:
            if settings.redis_conn:
                try:
                    settings.redis_conn.close()
                except Exception as why:
                    pass
            settings.redis_conn = redis.Redis(host=s.host, port=s.port, password=s.password,
                                              db=s.select_db)
            settings.redis_conn.info('status')
            return True
        except Exception as why:
            return False


def change_redis(setting_id: int, setting_db: int) -> bool:
    s = SettingsModel.query.filter_by(id=setting_id).first()
    if not s:
        return False
    SettingsModel.query.filter(SettingsModel.id != s.id).update({'is_select': False})
    s.select_db = setting_db
    s.is_select = True
    db.session.commit()
    return True


def get_redis():
    s = SettingsModel.query.filter_by(is_select=True).first()
    if s:
        change_redis_conn(s)


class RedisPagination(object):

    def __init__(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self._total = 0

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value
        # redis_conn.client_getname()

# print(redis_conn.info())

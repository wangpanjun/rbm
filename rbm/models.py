# -*- coding: utf-8 -*-

"""
jobsystem models.
"""
from rbm.app import db
from datetime import datetime


class SettingsModel(db.Model):

    __tablename__ = 'db_settings1'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=128), default='')
    host = db.Column(db.String(length=128), default='')
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String(length=32), default='')
    select_db = db.Column(db.Integer, default=0)
    is_select = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name='默认', host='localhost', port=6379, password='', is_select=0):
        self.name = name
        self.host = host
        self.port = port
        self.password = password
        self.is_select = is_select

    def info(self):
        return {
            'id': self.id,
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'password': self.password,
            'select_db': self.select_db,
            'is_select': self.is_select,
            'created_time': str(self.created_time)
        }


# if __name__ == '__main__':
db.drop_all()
db.create_all()
    # settings = SettingsModel()
    # settings.is_select = True
    # db.session.add(settings)
    # db.session.commit()

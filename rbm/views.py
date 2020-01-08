# -*- coding: utf-8 -*-

from flask import render_template, request, flash
from rbm.app import app, db
from rbm import settings
from rbm.models import SettingsModel

import json

from rbm.utils import change_redis, change_redis_conn
from rbm.handler import RedisValues


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the {0} field - {1}"
                  .format(getattr(form, field).label.text, error), 'error')


def _get_settings():
    select_st = SettingsModel.query.filter_by(is_select=1).first()
    data = []
    if select_st:
        queryset = SettingsModel.query.filter(SettingsModel.id != select_st.id)[:4]
        data.append(select_st.info())
    else:
        queryset = SettingsModel.query.filter()[:5]
    for o in queryset:
        data.append(o.info())
    # c = SettingsModel.query.all().count()
    # print(c)

    if data and not select_st:
        select_st = data[0]

    return select_st, data


@app.route("/", methods=["GET"])
def home():
    dbs = []
    select_st, data = _get_settings()
    f = change_redis_conn(select_st)
    info, error = {}, 1
    if f:
        error = 0
        info = settings.redis_conn.info()

    for i in range(16):
        v = info.get(f"db{i}", {})
        dbs.append({
            'db': i,
            'keys': v.get('keys', 0)
        })
    settings_count = SettingsModel.query.count()
    return render_template("home.html", show_st=data, dbs=dbs, info=info, error=error,
                           select_db=select_st.select_db if select_st else 0,
                           settings_count=settings_count)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/db", methods=['POST'])
def db_settings():
    data = request.form
    tmp = {}
    for i in data:
        tmp = json.loads(i)

    st_id = tmp.get('stId', 1)
    try:
        db_id = tmp.get('dbId', 0)
    except ValueError:
        db_id = 0
    change_redis(st_id, db_id)
    return "200"


@app.route("/keys")
def get_keys():
    q = request.args.get('q', '')
    try:  # 游标
        cur = int(request.args.get('cur'))
    except ValueError:
        cur = 0
    page_size = 10
    if not q:
        cursor, keys = settings.redis_conn.scan(cur, count=page_size)
    else:
        cursor, keys = settings.redis_conn.scan(cur, count=page_size, match=q)
    pipe = settings.redis_conn.pipeline()
    s_keys = []
    for key in keys:
        s_keys.append(key.decode('utf8'))
        pipe.type(key)

    s_types = [o.decode('utf8') for o in pipe.execute()]
    res = {
        'data': dict(zip(s_keys, s_types)),
        'cur': cur,
        'next_cur': cursor,
        'q': q
    }
    return json.dumps(res, ensure_ascii=False)


@app.route("/values", methods=['GET'])
def get_values():
    key = request.args.get('key')
    if not key:
        return "不存在"
    k_type = settings.redis_conn.type(key).decode('utf8')
    if k_type == 'none':
        return "不存在"
    func = getattr(RedisValues, f'{k_type}_get')
    if not func:
        return "不支持"
    data = func(key, request.args)
    return data


@app.route("/settings/<sid>", methods=['GET', 'POST', 'DELETE'])
def detail_setting(sid):
    if request.method.upper() == 'DELETE':
        SettingsModel.query.filter_by(id=sid).delete()
        db.session.commit()
        return "204"

    obj = {}
    if sid != 'new':
        s = SettingsModel.query.filter_by(id=sid).first()
        if s:
            obj = s.info()

    select_dbs = [i for i in range(16)]
    return render_template("adds.html", data=obj, select_dbs=select_dbs)


@app.route("/settings", methods=['GET'])
def list_settings():
    _, show_st = _get_settings()
    obj = {}
    sid = request.args.get('id', None)
    if sid:
        s = SettingsModel.query.filter_by(id=sid).first()
        if s:
            obj = s.info()
    res = [o.info() for o in SettingsModel.query.all()]
    dbs = []
    try:
        info = settings.redis_conn.info('Keyspace')
    except Exception:
        info = {}
    for i in range(16):
        v = info.get(f"db{i}", {})
        dbs.append({
            'db': i,
            'keys': v.get('keys', 0) if v else 0
        })
    settings_count = SettingsModel.query.count()
    select_dbs = [i for i in range(16)]
    return render_template("settings.html", data=obj, show_st=show_st, content=res, dbs=dbs,
                           cur=sid, settings_count=settings_count, select_dbs=select_dbs)


@app.route("/settings", methods=['POST'])
def setting_config():
    data = request.form
    tmp = {}
    for i in data:
        tmp = json.loads(i)
    if tmp['id']:
        s = SettingsModel.query.filter_by(id=tmp['id']).first()
    else:
        s = SettingsModel()
        db.session.add(s)
    s.is_select = True if int(tmp['is_select']) == 1 else False
    s.name = tmp['name']
    s.select_db = tmp['select_db']
    s.is_select = tmp['is_select']
    db.session.flush()
    if s.is_select:
        SettingsModel.query.filter(SettingsModel.id != tmp['id']).update({'is_select': False})
    s.password = tmp['password']
    s.host = tmp['host']
    s.port = tmp['port']
    db.session.commit()
    return str(s.id)

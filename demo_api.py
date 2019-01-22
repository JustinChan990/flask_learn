# -*- coding: utf-8 -*-

from flask import Flask, request
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql

#创建flask对象
app = Flask(__name__)

#配置flask配置对象中键：SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@192.168.18.11/baggins"

#配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#获取SQLAlchemy实例对象，接下来就可以使用对象调用数据

db = SQLAlchemy(app)

class Works(db.Model):
    __tablename__ = 'baggins_works'
    id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(100), unique=True, nullable=False)
    media_type = db.Column(db.Integer, nullable=False)


@app.route('/api/show_works', methods=['GET'])
def show_works():
    data_list = Works.query.all()
    return_list = []
    for data in data_list:
        return_list.append([data.id, data.work_name, data.media_type])
    return json.dumps(return_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

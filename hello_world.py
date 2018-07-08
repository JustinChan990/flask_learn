# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request
from flask import render_template

# set env to develop
os.environ.setdefault('FLASK_ENV', 'development')

# initialize Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world'


@app.route('/user/<username>')
def get_username(username):
    return 'hello! %s' % username


# URL如果不符合条件，将会返回404
@app.route('/book/<int:book_id>')
def get_bookid(book_id):
    return 'book id is %d' % book_id


@app.route('/path/<path:subpath>')
def get_subpath(subpath):
    return 'subpath is %s' % subpath


# get/post标准写法
@app.route('/method/', methods=['GET', 'POST'])
def show_method():
    print dir(request.method)
    if request.method == 'POST':
        #post_data = request.data
        post_data = request.get_data()
        json_data = json.loads(post_data)
        return 'POST name is %s' % json_data.get('name')
    elif request.method == 'GET':
        return 'GET'


@app.route('/tmpl/<string:name>')
def tmpl_demo(name):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# -*- coding: utf-8 -*-

import os
import json
from flask import Flask, request
from flask import render_template
from flask import make_response
from flask import session, url_for, escape, redirect
from werkzeug.utils import secure_filename

# set env to develop
os.environ.setdefault('FLASK_ENV', 'development')

# initialize Flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'username' in session:
        return 'hello world'
    else:
        return redirect(url_for('login'))


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
    if request.method == 'POST':
        #post_data = request.data
        post_data = request.get_data()
        json_data = json.loads(post_data)
        return 'POST name is %s' % json_data.get('name')
    elif request.method == 'GET':
        get_data = request.args.get('key', 'nothing')
        return 'GET key is %s' % get_data


@app.route('/upload/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        f = request.files['the_file']
        f.save('./upload_files/' + secure_filename(f.filename))
        return 'upload ok'


@app.route('/set_cookies/')
def set_cookies():
    client_cookie = request.cookies.get('username')
    resp = make_response(render_template('index.html'))
    if not client_cookie:
        resp.set_cookie('username', 'justin')
    return resp


@app.route('/tmpl/<string:name>')
def tmpl_demo(name):
    return render_template('index.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# -*- coding: utf-8 -*-

import json
import urllib2
import requests

demo_url = 'http://127.0.0.1:5000/method/'
data = json.dumps({'name': 'justin'})


def http_get():
    req = urllib2.Request(demo_url + '?key=jack')
    res = urllib2.urlopen(req)
    print res.read()


def http_post():
    req = urllib2.Request(demo_url, data=data)
    res = urllib2.urlopen(req)
    print res.read()


def http_post2():
    req = requests.post(demo_url, data=data)
    print req.text

http_get()
http_post()
http_post2()

# -*- coding: utf-8 -*-
"""
Copyright 2014, Gestalt LUR. All rights reserved.

A simple Blog framework.

"""

import json
import logging
import datetime
import time
import os

import requests
import redis
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

REDIS_URL = os.environ.get("REDIS_URL")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['POST', 'GET'])
def show_main_page():
    redis_conn = redis.StrictRedis(host=REDIS_URL, port=REDIS_PORT)
    post_list = redis_conn.lrange("post_list", 0, -1)

    return render_template('index.html',
                           post_list=post_list)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    pipe = redis.StrictRedis(host=REDIS_URL, port=REDIS_PORT).pipeline()
    pipe.get("title:%d" % post_id)
    pipe.get("post:%d" % post_id)
    pipe.get("time:%d" % post_id)
    title, post, time = pipe.execute()

    return render_template('post.html',
                           time=time, title=title, post=post)

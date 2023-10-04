#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：zzh
@Date    ：2023/8/9 21:56 
'''
import base64
import os


from flask import Flask
from .app import chat_bp


def create_app():
    chat = Flask(__name__, template_folder='../templates', static_folder='../static')
    chat.config['SECRET_KEY'] = base64.b64encode(os.urandom(24))
    chat.register_blueprint(chat_bp)
    return chat

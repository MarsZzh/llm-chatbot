#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：zzh
@Date    ：2023/8/9 22:31 
'''

from chat import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8010)
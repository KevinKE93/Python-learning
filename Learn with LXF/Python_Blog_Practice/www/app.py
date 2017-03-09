#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by kevin @ 2017-02-09 10:30


import logging
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

logging.basicConfig(level=logging.INFO)


# set index
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html', charset='UTF-8')


# request listen and print log in console
@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000……')
    return srv


# start web server
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

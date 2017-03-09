#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by kevin @ 2017-03-09 23:38


import time, uuid
from .orm import Model, StringField, IntegerField, BooleanField, FloatField, TextField


def next_id():
    return '%015d%s000' % (int(time.time()*1000), uuid.uuid4().hex)


class User:
    __table__ = 'users'
    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50')
    email = StringField(ddl='varchar(50')
    password = StringField(ddl='varchar(50')
    admin = BooleanField()
    name = StringField(ddl='varchar(50')
    image = StringField(ddl='varchar(500')
    created_time = FloatField(default=time.time())


class Blog:
    __table__ = 'blogs'
    id = StringField(primary_key=True, default=next_id(), ddl='varchar(50')
    user_id = StringField(ddl='varchar(50')
    user_name = StringField(ddl='varchar(50')
    user_image = StringField(ddl='varchar(500')
    name = StringField(ddl='varchar(50')
    summary = StringField(ddl='varchar(200')
    content = TextField()
    created_time = FloatField(default=time.time())


class Comment:
    __table__ = 'comments'
    id = id = StringField(primary_key=True, default=next_id(), ddl='varchar(50')
    blog_id = StringField(ddl='varchar(50')
    user_id = StringField(ddl='varchar(50')
    user_name = StringField(ddl='varchar(50')
    user_image = StringField(ddl='varchar(500')
    content = TextField()
    created_time = FloatField(default=time.time())

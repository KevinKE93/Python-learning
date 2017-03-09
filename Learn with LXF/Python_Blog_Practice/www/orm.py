#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by kevin @ 2017-03-08 10:30

import asyncio, aiomysql, logging


def log(sql, args=()):
    logging.info('SQL: %s' % sql)


@asyncio.coroutine
def create_mysql_pool(loop, **kwargs):
    logging.info('Create MySQL Connection pool…')
    global __pool
    __pool = yield from aiomysql.create_pool(
        # set necessary **kwargs for aiomysql.create_pool
        maxsize=kwargs.get('maxsize', 10),
        minsize=kwargs.get('minsize', 1),
        loop=loop,
        # set **kwargs for aiomysql.create_pool from create_mysql_pool's **kwargs
        host=kwargs.get('host', 'localhost'),
        port=kwargs.get('port', 3306),
        user=kwargs['user'],
        db=kwargs['db'],
        charset=kwargs.get('charset', 'utf-8'),
        autocommit=kwargs.get('autocommit', True)
    )


@asyncio.coroutine
def mysql_select(sql, args, size=None):
    log(sql, args)
    global __pool
    # get connection args
    with (yield from __pool) as connection:
        cursor = yield from connection.cursor(aiomysql.DictCursor)
        yield from cursor.execute(sql.replace('s', '%s'), args or ())
        if size:
            rs = yield from cursor.fetchmany(size)
        else:
            rs = yield from cursor.fetchall()
        yield from cursor.close()
        logging.info('rows returned : %s' % len(rs))
        return rs


@asyncio.coroutine
def mysql_execute(sql, args):
    log(sql)
    with (yield from __pool) as connection:
        try:
            cursor = yield from connection.cursor()
            affected_count = cursor.rowcount
            yield from cursor.close()
        except BaseException as e:
            raise
        return affected_count


def create_args_string(num):
    l = []
    for n in range(num):
        l.append('?')
    return ','.join(l)


class Field(object):
    def __init__(self, name, column_type, primary_key, defualt):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.defualt = defualt

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.name, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # ignore class self
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # get table name
        tablename = attrs.get('__table__', None) or name
        logging.info('found model: %s(table:%s)' % (name, tablename))
        # get all field and primary_key name
        mappings = dict()
        fields = []
        primarykey = None
        for k, v in attrs.item():
            if isinstance(v, Field):
                logging.info(' Found mapping:%s===>%s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # found primary key
                    if primarykey:
                        raise RuntimeError('Duplicate primary key for field:%s' % k)
                    primarykey = k
                else:
                    fields.append(k)
        if not primarykey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        # save the relationship between attrs and column
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tablename
        attrs['__primary_key__'] = primarykey
        attrs['__fields__'] = fields
        # build default SQL for SELECT, INSERT, UPDATE, DELETE:
        attrs['__select__'] = 'SELECT `%s`,%s from `%s` ' % (primarykey, ','.join(escaped_fields), tablename)
        attrs['__insert__'] = 'INSERT into `%s` (%s, `%s`) VALUES (%s)' % (
            tablename, ','.join(escaped_fields), primarykey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'UPDATE `%s` set %s WHERE `%s`=?' % (
            tablename, ','.join(map(lambda f: '`%s=?' % (mappings.get(f).name or f), fields)), primarykey)
        attrs['__delete__'] = 'DELETE from `%s` WHERE `%s`=?' % (tablename, primarykey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self.keys()
        except KeyError:
            raise AttributeError(r"'Model' Object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getvalue(self, key):
        return getattr(self, key, None)

    def getvalueordefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mapping__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('Using Default Value for %s %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    @asyncio.coroutine
    def findall(cls, where=None, args=None, **kwargs):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderby = kwargs.get('orderby', None)
        if orderby:
            sql.append('orderby')
            sql.append(orderby)
        limit = kwargs.get('limit', None)
        if limit is not None:
            sql.append(limit)
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value:%s' % str(limit))
        rs = yield from mysql_select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        rs = yield from mysql_select('%s where `%s`=?' % (cls.__select__, cls.primarykey), [pk], 1)
        if len(rs) == 0:
            return None
        else:
            return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getvalueordefault(), self.__fields__))
        args.append(self.getvalueordefault(self.__primary_key__))
        rows = yield from mysql_execute(self.__insert__, args)
        if rows != 1:
            logging.warning('Failed insert record: affected %s rows' % rows)

    @asyncio.coroutine
    def remove(self):
        args = [self.getvalue(self.__primary_key__)]
        rows = yield from mysql_execute(self.__delete__, args)
        if rows != 1:
            logging.warning('Failed to remove by primary key: affected %s rows' % rows)

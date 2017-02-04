#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def parama_test(a, b=0, *c, **d):
    print(a, b, c, d)


parama_test(1, 2, '3', 3, 5, xxx=99, xxxx='xxx')
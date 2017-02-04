#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

print('---This program is going to solve x from ax^2+bx+c=0---')


def solve_x(a, b=0, c=0):
    if a == 0:
        if b == 0:
            x = -c
            return x
        else:
            x = -c / b
            return x
    else:
        delta = b * b - 4 * a * c
        if delta > 0:
            x1 = (-b + math.sqrt(delta)) / (2 * a)
            x2 = (-b - math.sqrt(delta)) / (2 * a)
            return x1, x2
        elif delta == 0:
            x = -b / (2 * a)
            return x
        else:
            return '没有实数根'


print('请输入该方程的a、b、c：\n（b、c默认可不输入，为0）')
A = input('输入a')
B = input('输入b')
C = input('输入c')
result = solve_x(float(A), float(B), float(C))
print('你输入的方程式为：%sx^2+%sx+%s=0\n该方程的解为%s' % (A, B, C, result))

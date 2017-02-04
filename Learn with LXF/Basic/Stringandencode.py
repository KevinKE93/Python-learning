#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#On Python3,the default input type is str
s1 = int(input('输入去年的成绩：'))
s2 = int(input('输入今年的成绩：'))
delta = (s2 - s1)/s1*100
#print(delta)
if delta > 0.0:
    print('小明今年比去年提升了%.1f%%'%delta)
elif delta < 0.0:
    print('小明今年比去年退步了%.1f%%'%delta)
else:
    print('小明的成绩在原地踏步')

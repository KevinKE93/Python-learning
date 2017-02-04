#!/usr/bin/env python3
# -*- coding: utf-8 -*-
hight = float(input('请输入你的身高，单位米(m):'))
if hight == 0:
    print('身高不允许为0，程序将退出。')
    exit()
weight = float(input('请输入你的体重，单位千克(kg):'))
BMI = weight / (hight * hight)
if BMI <= 0:
    print('请输入正确的身高、体重')
elif BMI < 18.5:
    print('你的身高%.2f米,体重%.2f千克\nBMI指数为:%.2f,%s' % (hight, weight, BMI, '过轻'))
elif BMI < 25:
    print('你的身高%.2f米,体重%.2f千克\nBMI指数为:%.2f,%s' % (hight, weight, BMI, '正常'))
elif BMI < 28:
    print('你的身高%.2f米,体重%.2f千克\nBMI指数为:%.2f,%s' % (hight, weight, BMI, '过重'))
elif BMI < 32:
    print('你的身高%.2f米,体重%.2f千克\nBMI指数为:%.2f,%s' % (hight, weight, BMI, '肥胖'))
else:
    print('你的身高%.2f米,体重%.2f千克\nBMI指数为:%.2f,%s' % (hight, weight, BMI, '严重肥胖'))

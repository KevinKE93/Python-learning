#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### completed verson
def hanoi(n, start, buffer, end):
    sticks = {start: [], buffer: [], end: []}
    sticks[start] = list(range(1, n + 1))
    print(sticks)
    if n == 1:
        sticks[end].append(sticks[start].pop())
        print('从', start, '--移动-->', end, sticks)
    else:
        hanoi(n - 1, start, end, buffer)
        print('从', start, '--移动-->', end, sticks)
        hanoi(n - 1, buffer, start, end)


num = int(input('输入你想计算的海诺塔层数：'))
a, b, c = 'A', 'B', 'C'
while num <= 0:
    print('层数必须为大于0的整数\n')
    num = int(input('请输入汉诺塔的层数：'))

hanoi(num, a, b, c)

### Simple version
# def hanoi(n, start, buffer, end):
#     if n == 1:
#         print('从', start, '--移动-->', end)
#         return
#     else:
#         hanoi(n - 1, start, end, buffer)
#         print('从', start, '-->', end)
#         hanoi(n - 1, buffer, start, end)
#
#
# hanoi(2, 'a', 'b', 'c')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### completed verson-Bug
def hanoi(n, **kw):
    if n == 1:
        kw[c].insert(0,kw[a][-1])
        kw[a].pop()
        print('从', a, '--移动1-->', c, ':\n', kw)
        return
    else:
        hanoi(n - 1, **kw)
        print('从', a, '--移动2-->', b, ':\n', kw)
        hanoi(n - 1, **kw)
        print('从', b, '--移动3-->', c, ':\n', kw)
        return


num = int(input('输入你想计算的海诺塔层数：'))
a, b, c = 'A', 'B', 'C'
while num <= 0:
    print('层数必须为大于0的整数\n')
    num = int(input('请输入汉诺塔的层数：'))
sticks = {a: list(range(1, num + 1)), b: [], c: []}
print('这是你输入的海诺塔\n', sticks, "\n--------")
hanoi(num, **sticks)

### completed verson
def hanoi(n, start, buffer, end):
  sticks = {start: [], buffer: [], end: []}
  sticks[start] = list(range(1, n + 1))
  if n == 1:
      sticks[end].append(sticks[start].pop())
      print('从', start, '--移动-->', end)
      return
  else:
      hanoi(n - 1, start, end, buffer)
      print('从', start, '--移动-->', end)
      hanoi(n - 1, buffer, start, end)
      return

num = int(input('输入你想计算的海诺塔层数：'))
a, b, c = 'A', 'B', 'C'
while num <= 0:
  print('层数必须为大于0的整数\n')
  num = int(input('请输入汉诺塔的层数：'))

hanoi(num, a, b, c)





### Simple version
def hanoi(n, start, buffer, end):
    if n == 1:
        print('从', start, '--移动-->', end)
        return
    else:
        hanoi(n - 1, start, end, buffer)
        print('从', start, '--移动-->', end)
        hanoi(n - 1, buffer, start, end)


hanoi(2, 'a', 'b', 'c')

import time
import calendar


def my_cal(n):
    year = int(n / 10000)
    month = int((n / 100) % 100)
    if n == 0:
        year = time.localtime().tm_year
        month = time.localtime().tm_mon
        day_list = calendar.monthcalendar(year, month)
    else:
        day_list = calendar.monthcalendar(year, month)
    print('%4s年%1s月' % (str(year), str(month)), calendar.weekheader(4))
    for i in day_list:
        print('  week%s' % str(day_list.index(i) + 1), end='')
        for j in i:
            if j == 0:
                j = ' '
            print('%5s' % j, end='')
        print('\n', end='')

lookup = int(input('\n输入你要查询的年月(日)，例如20161011，直接输入0为查询当前月:\n'))
my_cal(lookup)

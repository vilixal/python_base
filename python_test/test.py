line = '[2018-05-17 01:57:16.665804] NOK'
date, time, res = line.split(' ')
dt = date + ' ' + time[:5] + time[-1:]
print(date)
print(time)
print(res)
print(dt)

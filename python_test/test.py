res = {'bulls': 0, 'cows': 0}
num='5333'
number='3355'
i = 0
for numberi in number:
    if numberi == num[i]:
        res['bulls'] += 1

    elif numberi in num:
        res['cows'] += 1
    i += 1
print(res)
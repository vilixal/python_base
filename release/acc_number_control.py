sum1=0
a='101040102810945370000060'
b='713071371371371371371371'
for i in range(24):
    sum1+= int(str(int(a[i])*int(b[i]))[-1])
    print(sum1)
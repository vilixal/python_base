stat = {'a':1,'b':2,'e':5,'c':3}
print(stat)
list = list(stat.items())
print(list)
list.sort()
print(list)
print()
print(sorted(stat.items()))

def sort_key(e):
    return e[1]

print(sorted(stat.items(),key=sort_key))

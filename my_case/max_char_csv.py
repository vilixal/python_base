import re

maxGestDepoID, maxNumberList, maxNumberProduction, maxDateDecision, maxFsspKey = ('0',) * 5


def maxline(att, maxatt):
    if len(att) >= len(maxatt):
        return att
    else:
        return maxatt


with open(r'D:\temp\pochta\акбарс\Новая папка (2)\Не закрытые ссп_ALL.csv') as file:
    for line in file:
        match=None
        GestDepoID, NumberList, NumberProduction, DateDecision, FsspKey,*args = line.split(';')
        maxGestDepoID = maxline(GestDepoID,maxGestDepoID)
        maxNumberList = maxline(NumberList, maxNumberList)
        maxNumberProduction=maxline(NumberProduction, maxNumberProduction)
        maxDateDecision=maxline(DateDecision, maxDateDecision)
        maxFsspKey=maxline(FsspKey, maxFsspKey)
        match = re.search(r'[\D]+',FsspKey.strip())
        if match:
            print(FsspKey)
print(len(maxGestDepoID), len(maxNumberList), len(maxNumberProduction), len(maxDateDecision), len(maxFsspKey))

import re

input_file='test.txt'
pars_start=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{4} \('
pars_attach=r'\(ATT\_'
file = open(input_file,'r',encoding='utf-8')
first_line=False
for line in file:
    if first_line==False and re.match(pars_start,line):
        start_time,proc,operand=line.split()
        tread_full,num_tread=proc[1:-1].split(sep='#')
        print(start_time,tread_full, num_tread,operand)
        first_line=True
        continue
    elif first_line==True and re.search(pars_attach,line):
        alias,attach,user,*_=line.split()
        attach=attach[1:-1]
        user=user[:user.index(':')]
        print(alias,attach,user)
        first_line = False


file.close()    

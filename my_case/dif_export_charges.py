import re
import pprint
from datetime import datetime,time,timedelta

file_temp='''Строка   56894: 10.03.25 12:31:49.375,https-jsse-nio-8443-exec-140,INFO,LogDocFlowLogger,Обработка документа (UNIFO_EXPORT_CHARGE_REQUEST, ID=6808017712753314637) класс 1000 статус 1: Запрос экспорта начислений из ГИС ГМП (Документ: Запрос экспорта начислений из ГИС ГМП(Новый)
10.03.25 12:31:54.021,dx2-a.27.getresponse-9388,DEBUG,UnifoExportChargeResponseSmev3FromJaxConverter,Обработка ответа на запрос экспорта начислений 6808017712753314637

	Строка  122889: 10.03.25 12:31:54.304,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,locked document 6808017712753314637
	Строка  122890: 10.03.25 12:31:54.304,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,full release lock 1047050654 of 6808017712753314637
	Строка  122894: 10.03.25 12:31:54.305,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,locked document 6808017712753314637
	Строка  122895: 10.03.25 12:31:54.305,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,full release lock 1047050654 of 6808017712753314637
	Строка  122899: 10.03.25 12:31:54.306,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,locked document 6808017712753314637
	Строка  122900: 10.03.25 12:31:54.306,dx2-a.27.getresponse-9388,DEBUG,GisgmpDocumentSynchronizer,full release lock 1047050654 of 6808017712753314637
	Строка  122901: 10.03.25 12:31:54.306,dx2-a.27.getresponse-9388,DEBUG,DxEnvObject,ПГД. Env 471493729, setting DataMessage, documentId=6808017712753314637, metaobjectname=UNIFO_EXPORT_CHARGE_REQUEST; documentId=6808017712753314637; id=471493729; metaobjectname=UNIFO_EXPORT_CHARGE_REQUEST
	Строка  137528: 10.03.25 12:31:55.811,dx2-t.4302.env_execute-2074,WARN,DocumentExecutor,Временный сбой обработки документа. Документ на статусе "Запрос выполнен" (310) уже обработан (не находится на статусе ожидания обработки - 800). Документ: 471493729 -> UNIFO_EXPORT_CHARGE_REQUEST#6808017712753314637; docstatus_caption=Запрос выполнен; docstatusid=310; env.docMetaobjectname=UNIFO_EXPORT_CHARGE_REQUEST; env.documentId=6808017712753314637; env.id=471493729; env.sender=GISGMP_SMEV3_CHARGES:ГИС_ГМП_СМЭВ3; env.sender.department=null; env.sender.organization=ГИС_ГМП_СМЭВ3; env.sender.protocol=GISGMP_SMEV3_CHARGES; event=execute
	Строка  180754: 10.03.25 12:31:59.500,https-jsse-nio-8443-exec-53,DEBUG,IDBankUnifoServiceImpl,Обработка ответа (ID:6808017712753315286) на запрос экспорта начислений (ID:6808017712753314637)
	Строка  180755: 10.03.25 12:31:59.500,https-jsse-nio-8443-exec-53,DEBUG,IDBankUnifoServiceImpl,Ответ на запрос экспорта начислений (ID:6808017712753314637) существует. Подготовка ответа...
	Строка  180756: 10.03.25 12:31:59.506,https-jsse-nio-8443-exec-53,DEBUG,IDBankUnifoServiceImpl,Ответ на запрос экспорта начислений (ID:6808017712753314637) подготовлен.'''

file_temp2=file_temp.split('\n')

process_dict = {}
with open(r'D:\temp\pochta\совком\НГ1003\logs.backup.2025-03-10_1329', encoding='utf8') as file:
    for line in file:
        match = re.search(
            r'([0-9]{2}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}),https-jsse-nio-8443-exec-[\d]+,INFO,LogDocFlowLogger,Обработка документа \(UNIFO_EXPORT_CHARGE_REQUEST, ID=(\d+)\) класс 1000 статус 1:',
            line)
        if match:
            date_process = datetime.strptime(match.group(1), '%d.%m.%y %H:%M:%S.%f')
            a=match.group(2)
            if match.group(2):
                process_dict[match.group(2)]=[0,0,0]
                process_dict[match.group(2)][0] = date_process
        match_get = re.search(
            r'([0-9]{2}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}),dx2-a.27.getresponse-[\d]+,DEBUG,UnifoExportChargeResponseSmev3FromJaxConverter,Обработка ответа на запрос экспорта начислений ([\d]+)',
            line)
        if match_get:
            date_get = datetime.strptime(match_get.group(1), '%d.%m.%y %H:%M:%S.%f')
            if match_get.group(2):
                process_dict[match_get.group(2)][1] = date_get
        match_put = re.search(
            r'([0-9]{2}.[0-9]{2}.[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}),https-jsse-nio-8443-exec-\d+,DEBUG,IDBankUnifoServiceImpl,Ответ на запрос экспорта начислений \(ID:(\d+)\) существует. Подготовка ответа',
            line)
        if match_put:
            date_put = datetime.strptime(match_put.group(1), '%d.%m.%y %H:%M:%S.%f')
            if match_put.group(2):
                process_dict[match_put.group(2)][2] = date_put

dtime = timedelta(seconds=11)

for i, keys in process_dict.items():
    try:
        delta = process_dict[i][2] - process_dict[i][0]
        if delta>dtime:
            #process_dict[i].append(delta)
            print(i,str(process_dict[i][0]),str(delta))
    except:
        pass


#pprint.pp(process_dict)


import re

file = '''2025-02-19T10:28:50.9320 (1435799:0x7fb7adef8c40#9) EXECUTE_STATEMENT_FINISH
	ncore-bank (ATT_1388275, NT_APP9:NONE, WIN1251, TCPv4:127.0.0.1/56536)
	NCORE:[WS-DX] - iD-Банк v1.9.26.0 - IDBankUnifoService (IP:10.60.82.134):1497598
		(TRA_671260667, READ_COMMITTED | READ_CONSISTENCY | WAIT 10 | READ_ONLY)

Statement 3095657:
-------------------------------------------------------------------------------
select max(g) from (
select max(rpl$generation) g from r$SYS_GROUPMEMBER
union all
select max(rpl$generation) g from r$SYS_ROLE
union all
select max(rpl$generation) g from r$SYS_ROLE_OBJECT_GROUP
union all
select max(rpl$generation) g from r$SYS_USER_ROLES)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PLAN (R$SYS_GROUPMEMBER ORDER R$SYS_GROUPMEMBER, R$SYS_ROLE ORDER R$SYS_ROLE, R$SYS_ROLE_OBJECT_GROUP ORDER R$SYS_ROLE_OBJECT_GROUP, R$SYS_USER_ROLES ORDER R$SYS_USER_ROLES)
1 records fetched without sorting
      0 ms, 12 fetch(es)

Table                              Natural     Index    Update    Insert    Delete
**********************************************************************************
R$SYS_ROLE                                         1                                                                                                                                  
R$SYS_USER_ROLES                                   1                                                                                                                                  

2025-02-19T10:28:50.8990 (1435799:0x7fb791649ac0#11430) EXECUTE_STATEMENT_FINISH
	ncore-bank (ATT_1387418, SYSDBA:NONE, WIN1251, TCPv4:127.0.0.1/40768)
	NCORE:DX_Adapter[C] Soap EClient:1497598
		(TRA_671260587, READ_COMMITTED | READ_CONSISTENCY | WAIT 10 | READ_WRITE)

Statement 348230:
-------------------------------------------------------------------------------
UPDATE DX_LOG SET ADAPTER_METANAME = ?, ADAPTER_ID = ?, DOCUMENT_ID = ?, EVENT_XML_LOCAL_NAME = ?, DATA_LENGTH = ?, ATTACH_COUNT = ?, ATTACH_SIZE = ? WHERE ID = ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PLAN (DX_LOG INDEX (PK_DX_LOG))

param0 = varchar(63), "DX_ADAPTER_SMEV_3_GISGMP"
param1 = bigint, "26"
param2 = bigint, "6808017711037940673"
param3 = varchar(255), "GetResponseRequest"
param4 = bigint, "3504"
param5 = integer, "<null>"
param6 = bigint, "<null>"
param7 = bigint, "180952151"

0 records fetched without sorting
      0 ms, 16 fetch(es), 3 mark(s)

Table                              Natural     Index    Update    Insert    Delete
**********************************************************************************
DX_LOG                                             1         1                                                                                                                        

2025-02-19T10:28:50.8990 (1435799:0x7fb7aed3b040#23) EXECUTE_STATEMENT_FINISH
	ncore-bank (ATT_1388260, NT_APP9:NONE, WIN1251, TCPv4:127.0.0.1/56414)
	NCORE:[WS-DX] - iD-Банк v1.9.26.0 - IDBankUnifoService (IP:10.60.82.134):1497598
		(TRA_671260385, READ_COMMITTED | READ_CONSISTENCY | WAIT 10 | READ_ONLY)

Statement 3092523:
-------------------------------------------------------------------------------
SELECT DOCSTATUS.CAPTION,DOCSTATUS.COLOR,DOCSTATUS.DOCUMENTCLASS_ID,DOCSTATUS.ID,DOCSTATUS.PROCTREE
FROM DOCSTATUS DOCSTATUS

 optimize for all rows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PLAN (DOCSTATUS NATURAL)
1372 records fetched without sorting
      3 ms, 1401 fetch(es)

Table                              Natural     Index    Update    Insert    Delete
**********************************************************************************
DOCSTATUS                             1372                                              '''

# dict timestamp,process_id,thread_id,thread_number,event,db,attachment,user,process_name,transaction,sql_text,time_execute
timestamp, process_id, thread_id, thread_number, event, db, attachment, user, process_name, transaction, sql_text, time_execute = (0,) * 12
first_line = True
first_line_sql = False
i=0
lines = file.split('\n')
trace
for line in lines:
    match_timestamp = re.match(r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{4})\s\((?P<process_id>\d+):(?P<thread_id>\w+)#(?P<thread_number>\d+)\)\s(?P<event>\w+)',line)
    if match_timestamp:
        timestamp = match_timestamp.group("timestamp")
        process_id = match_timestamp.group("process_id")
        thread_id = match_timestamp.group("thread_id")
        thread_number = match_timestamp.group("thread_number")
        event = match_timestamp.group("event")
        first_line = False
        continue
    match_att=re.search(r'(?P<db>[-a-zA-Z0-9_]+)\s\(ATT_(?P<attachment>\d+),\s(?P<user>[-a-zA-Z0-9_]+):\w+,\s\w+,\s',line)
    if match_att:
        db=match_att.group('db')
        attachment = match_att.group('attachment')
        user = match_att.group('user')
        continue
    match_proc=re.search(r'(?P<process_name>NCORE:[\w\s\[\]()-]+):\d+$',line)
    if match_proc:
        process_name=match_proc.group('process_name')
    match_transaction = re.search(r'\(TRA_(?P<transaction>\d+),\s\w+\s\|\s\w+\s\|\s\w+\s\d+\s\|\s\w+\)$', line)
    if match_transaction:
        transaction=match_transaction.group('transaction')
    match_sql=re.search(r'[-]{79}',line)
    match_end_sql=re.search(r'[\^]{79}',line)
    if match_end_sql:
        first_line_sql=False
    if first_line_sql:
        sql_text+=line
    if match_sql:
        first_line_sql=True
        sql_text=''
        match_sql=None
    match_execute=re.search(r'(?P<time_execute>\d+)\sms,\s\d+\s',line)
    if match_execute:
        time_execute=match_execute.group('time_execute')
        i+=1
        first_line = True


print(timestamp, process_id, thread_id, thread_number, event, db, attachment, user, process_name, transaction, sql_text,
      time_execute)

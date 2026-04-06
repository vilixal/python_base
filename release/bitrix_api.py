from pprint import pprint

import requests
import csv
from datetime import datetime, timedelta

from my_case.bitrixt_test import department_get

# Настройки
BITRIX24_DOMAIN = "icamgrp.bitrix24.ru"
WEBHOOK_TOKEN = "ivhpba6cqb56ygx4"

def get_method(name,**parameters):
    """
    Параметры:
        name: 'department.get','user.get','tasks.task.list','task.elapseditem.getlist',
        filter: dict - {'>=CLOSED_DATE':'2026-03-28T13:45:48+03:00'},
        order: dict - {'ID':'ASC'}
    """
    url = f"https://{BITRIX24_DOMAIN}/rest/36/{WEBHOOK_TOKEN}/{name}"
    formated_parameters = {'start':-1}
    all_data=[]
    for key, value in parameters.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                formated_parameters[f'{key}[{subkey}]'] = subvalue
        else:
            formated_parameters[key] = value
    while True:
        response = requests.get(url,params=formated_parameters)
        data = response.json()
        result_list=[]
        if "result" in data:
            result = data["result"]
            if isinstance(result, dict):
                for key, value in data["result"].items():
                    result_list.extend(value)
            else:
                result_list=result
            #Если список результатов пустой - возвращаем функцию
            if not result_list:
                return all_data
            #Преобразование в верхний регистр словарей внутри списка
            for x in range(len(result_list)):
                result_list[x] = {k.upper(): v for k, v in result_list[x].items()}
            #Дополняем список данных и получаем максимальное ID
            all_data.extend(result_list)
            MAX_ID = max(int(item['ID']) for item in result_list)
            formated_parameters['filter[>ID]']=MAX_ID
        else:
            break
    return all_data


#tasks=get_method('tasks.task.list',filter={'>=CLOSED_DATE':'2026-03-28T13:45:48+03:00','STATUS': '5'},order={'ID':'ASC'})
users=get_method('user.get' ,filter={'ACTIVE': True},order={'ID':'ASC'})
#departments = get_method('department.get' ,filter={'ACTIVE': True})
pprint(users)

#
#
#
# def department_get():
#     url = f"https://{BITRIX24_DOMAIN}/rest/36/{WEBHOOK_TOKEN}/department.get.json"
#     response = requests.get(url)
#     data = response.json()
#     return data
#
# def user_get():
#     url = f"https://{BITRIX24_DOMAIN}/rest/36/{WEBHOOK_TOKEN}/user.get.json"
#     all_user = []
#     MIN_ID = 0
#     while True:
#         params = {
#             "filter[ACTIVE]": True,
#             "order": "ASC",
#             "start": MIN_ID
#         }
#         response = requests.get(url, params=params)
#         data = response.json()
#         if "result" in data:
#             users = data["result"]
#             if users:
#                 all_user.extend(users)
#                 MIN_ID = MIN_ID + 50
#             else:
#                 break
#         else:
#             break
#     dep_sort={}
#     final_all_user = {}
#     departments=department_get()
#     for department_dict in departments["result"]:
#         dep_sort[department_dict["ID"]]=department_dict["NAME"]
#     for user in all_user:
#         user_pars = [user["LAST_NAME"] + ' ' + user["NAME"],dep_sort[str(user["UF_DEPARTMENT"][0])]]
#         final_all_user[user["ID"]] = user_pars
#     return final_all_user
#
#
# def get_tasks():
#     url = f"https://{BITRIX24_DOMAIN}/rest/36/{WEBHOOK_TOKEN}/tasks.task.list.json"
#     first_day = datetime(2025, 12, 25)
#     last_day = datetime(2026, 1, 1)
#     first_day_str = first_day.strftime("%Y-%m-%dT%H:%M:%S+03:00")
#     last_day_str = last_day.strftime("%Y-%m-%dT%H:%M:%S+03:00")
#     all_tasks = []
#     MIN_ID = 0
#     while True:
#         params = {
#             "filter[STATUS]": 5,
#             "filter[>=CLOSED_DATE]": first_day_str,
#             "filter[<=CLOSED_DATE]": last_day_str,
#             "filter[>ID]": MIN_ID,
#             "select[]": ["ID", "TITLE", "GROUP_ID", "CLOSED_DATE", "ALLOW_TIME_TRACKING"],
#             "order[ID]": "ASC",
#             "params[WITH_TIMER_INFO]": True,
#             "start": "-1"
#         }
#         response = requests.get(url, params=params)
#         data = response.json()
#         if "result" in data and "tasks" in data["result"]:
#             tasks = data["result"]["tasks"]
#             if tasks:
#                 all_tasks.extend(tasks)
#                 MIN_ID = max(int(item['id']) for item in tasks)
#             else:
#                 break
#         else:
#             break
#     return all_tasks
#
#
# def get_time_tracking_report(TASK_ID):
#     url = f"https://{BITRIX24_DOMAIN}/rest/36/{WEBHOOK_TOKEN}/task.elapseditem.getlist.json"
#     params = {
#         "TASK_ID": TASK_ID
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data
#
#
# report = []
# report_task = get_tasks()
# report_user = user_get()
# for task in report_task:
#     print('зашли в task', task['id'], task["allowTimeTracking"], 'закрыт',task["closedDate"])
#     if task["allowTimeTracking"] == 'Y':
#         #если признак учета времени, вызываем сбор учета времени по задаче
#         report_time = get_time_tracking_report(task['id'])
#         #временный словарь для группировки по минутам
#         temp_dict = {}
#         temp_developer = set()
#         alarm={}
#         for task_time in report_time['result']:
#             if 'Отдел разработки' in report_user[task_time['USER_ID']][1]:
#                 temp_developer.add(report_user[task_time['USER_ID']][0])
#             dt = datetime.fromisoformat(task["closedDate"])
#             closedDate = dt.strftime('%d.%m.%Y %H:%M:%S')
#             ##логика формирования ключей для посчета минут
#             key = (report_user[task_time['USER_ID']][1],report_user[task_time['USER_ID']][0], task_time['TASK_ID'], task["title"], task["group"]["name"],
#                    closedDate)
#             if key in temp_dict:
#                 temp_dict[key] += int(task_time['MINUTES'])
#             else:
#                 temp_dict[key] = int(task_time['MINUTES'])
#             ##логика формирования ключей для посчета минут
#
#             if int(task_time['MINUTES'])>480:
#                 hours = int(task_time['MINUTES']) // 60
#                 mins = int(task_time['MINUTES']) % 60
#                 if report_user[task_time['USER_ID']][0] in alarm:
#                     alarm[report_user[task_time['USER_ID']][0]] += ', >'+f"{hours}:{mins:02d}"
#                 else:
#                     alarm[report_user[task_time['USER_ID']][0]] = '>'+f"{hours}:{mins:02d}"
#         for key, minutes in temp_dict.items():
#             print_alarm = None
#             if alarm:
#                 print_alarm=alarm.get(key[1])
#             hours = int(minutes) // 60
#             mins = int(minutes) % 60
#             report.append([
#                 key[0], key[1], key[2], key[3], key[4], key[5],minutes,f"{hours}:{mins:02d}",print_alarm,', '.join(map(str, temp_developer)) if 'Отдел тестирования' in key[0] else ''
#             ])
#
# with open('bitrix_final_kv1(dec).csv', 'w', newline='', encoding='cp1251') as out_file:
#     writer = csv.writer(out_file, quotechar='"', delimiter=';')
#     writer.writerow(['Отдел', 'Сотрудник', 'ИД задачи', 'Задача', 'Группа', 'Дата закрытия', 'Время (минуты)','Время (часы)','Внимание! Внутри есть подозирительное время', 'Разработка (для ОТ)'])
#     for line in report:
#         writer.writerow(line)

# перепроверить 122900
# report.append([report_user[task_time['USER_ID']],task_time['TASK_ID'],task["title"], task["group"]["name"],task["closedDate"], task_time['MINUTES']])

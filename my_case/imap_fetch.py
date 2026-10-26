import imaplib
import email
import sys
import ssl
import time

# === НАСТРОЙКИ ===
IMAP_SERVER = 'imap.yandex.ru'
EMAIL_ACCOUNT = 'support@id-sys.ru'
PASSWORD = 'qcnrsphdfgjxwlpw'  # Для Яндекса лучше использовать пароль приложения
SOURCE_FOLDER = '&BBwEMARCBDIENQQ1BDI-'
QUARANTINE_FOLDER = 'Quarantine_Broken|matv_q'  # Папка, куда будем складывать "битые" письма

# Список UID, которые нужно проверить (из ваших логов Thunderbird)
#TARGET_UIDS = [416, 420, 421, 422]


def process_emails():
    # Подключение с SSL
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, ssl_context=ssl.create_default_context())
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        print(f"Успешный вход: {EMAIL_ACCOUNT}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return

    # status, folders = mail.list()
    # for folder in folders:
    #     print(folder.decode('utf-8'))

    # Выбор исходной папки
    status, response = mail.select(SOURCE_FOLDER)
    if status != 'OK':
        print(f"Не удалось открыть папку {SOURCE_FOLDER}: {response}")
        return

    # Проверяем/создаем папку карантина
    status, _ = mail.select(QUARANTINE_FOLDER)
    if status != 'OK':
        print(f"Папка {QUARANTINE_FOLDER} не найдена")
        #print(f"Создаем папку {QUARANTINE_FOLDER}...")
        #mail.create(QUARANTINE_FOLDER)

    mail.select(SOURCE_FOLDER)  # Возвращаемся в исходную папку

    status, data = mail.uid('search', None, 'ALL')

    uid_list=[]

    if status == 'OK':
        # data[0] — это байтовая строка, например b'1 2 3 4 5'
        uid_string = data[0].decode('utf-8')

        if uid_string:
            # Разбиваем строку по пробелам и преобразуем в список целых чисел
            uid_list = [int(uid) for uid in uid_string.split()]
            print(f"Найдено {len(uid_list)} писем в папке {SOURCE_FOLDER}.")
            print(f"Первые 10 UID: {uid_list[:10]}")
            print(uid_list)
        else:
            print("Папка пуста.")
    else:
        print(f"Ошибка поиска: {data}")

    TARGET_UIDS=uid_list

    for uid in TARGET_UIDS:
        # if uid<7081:
        #     continue
            
        print(f"\n--- Проверка UID: {uid} ---")

        # Пытаемся получить всё письмо целиком
        try:
            status, data = mail.uid('fetch', str(uid), '(RFC822)')
        except imaplib.IMAP4.abort as e:
            print(f"Соединение разорвано при обработке UID {uid}: {e}")
            # Переподключаемся и повторяем операцию для этого UID
            mail = reconnect_and_retry(mail, uid)
            status, data = mail.uid('fetch', str(uid), '(RFC822)')

        if status == 'OK' and data[0] is not None:
            # Если сервер вернул данные, пробуем распарсить
            try:
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Проверяем, есть ли вообще тема и отправитель (признак успешного чтения)
                subject = msg.get('Subject', 'Без темы')
                sender = msg.get('From', 'Неизвестный отправитель')

                print(f"[УСПЕХ] Письмо прочитано. Тема: {subject}, От: {sender}")

                # (Опционально) Здесь можно сохранить вложения на диск
                # for part in msg.walk():
                #     if part.get_content_maintype() == 'multipart':
                #         continue
                #     if part.get('Content-Disposition') is None:
                #         continue
                #     filename = part.get_filename()
                #     if filename:
                #         with open(filename, 'wb') as f:
                #             f.write(part.get_payload(decode=True))

            except Exception as e:
                print(f"[ОШИБКА ПАРСИНГА] Сервер отдал данные, но письмо повреждено: {e}")
                move_to_quarantine(mail, uid)
        else:
            # Если сервер вернул NO или BAD — письмо не читается
            print(f"[ОШИБКА ЧТЕНИЯ] Сервер не смог отдать письмо UID {uid}. Ответ: {data}")
            move_to_quarantine(mail, uid)

    mail.logout()


def move_to_quarantine(mail, uid):
    """Функция для перемещения письма в карантин (copy + delete)"""
    print(f"--> Перемещаем UID {uid} в папку {QUARANTINE_FOLDER}...")

    # 1. Копируем письмо в карантин
    try:
        copy_status, copy_data = mail.uid('copy', str(uid), QUARANTINE_FOLDER)
    except imaplib.IMAP4.abort as e:
        print(f"Соединение разорвано при обработке UID {uid}: {e}")
        # Переподключаемся и повторяем операцию для этого UID
        mail = reconnect_and_retry(mail, uid)
        copy_status, copy_data = mail.uid('copy', str(uid), QUARANTINE_FOLDER)

    if copy_status == 'OK':
        # 2. Помечаем исходное письмо как удаленное
        try:
            mail.uid('store', str(uid), '+FLAGS', '(\\Deleted)')
        except imaplib.IMAP4.abort as e:
            print(f"Соединение разорвано при обработке UID {uid}: {e}")
            # Переподключаемся и повторяем операцию для этого UID
            mail = reconnect_and_retry(mail, uid)
            mail.uid('store', str(uid), '+FLAGS', '(\\Deleted)')
        print(f"    Успешно перемещено.")
    else:
        print(f"    Не удалось скопировать в карантин. Ответ: {copy_data}")


def reconnect_and_retry(old_mail, uid):
    """Закрывает старое соединение, создает новое и повторяет операцию"""
    print("Переподключение к серверу...")
    try:
        old_mail.shutdown()  # Принудительно закрываем старое
    except:
        pass

    # Небольшая пауза, чтобы сервер не счел новое подключение атакой
    time.sleep(2)

    new_mail = imaplib.IMAP4_SSL(IMAP_SERVER, ssl_context=ssl.create_default_context())
    new_mail.login(EMAIL_ACCOUNT, PASSWORD)
    new_mail.select(SOURCE_FOLDER)

    return new_mail


if __name__ == '__main__':
    process_emails()
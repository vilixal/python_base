import base64

def decode_imap_utf7(s):
    if not s:
        return s
    res = []
    i = 0
    while i < len(s):
        if s[i] == '&':
            j = i + 1
            if j < len(s) and s[j] == '-':
                # Специальный случай: '&-' означает просто '&'
                res.append('&')
                i = j + 1
                continue
            # Ищем закрывающий дефис
            while j < len(s) and s[j] != '-':
                j += 1
            if j < len(s):
                # Извлекаем закодированную часть
                b64_part = s[i+1:j].replace(',', '/')
                # Добавляем padding для base64
                padding = '=' * ((4 - len(b64_part) % 4) % 4)
                try:
                    decoded = base64.b64decode(b64_part + padding).decode('utf-16-be')
                    res.append(decoded)
                except Exception:
                    res.append(s[i:j+1]) # Если ошибка, оставляем как есть
                i = j + 1
            else:
                res.append(s[i:])
                break
        else:
            res.append(s[i])
            i += 1
    return ''.join(res)

if __name__ == '__main__':
    print(decode_imap_utf7('&BBwEMARCBDIENQQ1BDI-'))
    # (\HasNoChildren \Unmarked)
    # "|" "&BB4EMQRJBDUENQ-"
    # (\HasNoChildren \Unmarked)
    # "|" "&BBIEMARBBDgEOwRMBDUEMg-"
    # (\HasNoChildren \Unmarked)
    # "|" "&BBgEOwRMBDgEPQ-"
    # (\HasNoChildren \Unmarked)
    # "|" "&BBoEQwQ7BDgEOgQ+BDI-"
    # (\HasNoChildren \Marked)
    # "|" "&BBwEMARCBDIENQQ1BDI-"
    # (\HasNoChildren \Unmarked)
    # "|" "&BCEEQgQwBEAEPgQyBD4EOQRCBD4EMg-"
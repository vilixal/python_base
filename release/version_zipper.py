# -*- coding: utf-8 -*-
"""
Скрипт архивации последней версии приложения iDБанк на FTP-шару.
Шифрование: ZipCrypto (совместимо с unzip в Linux, WinRAR, Explorer).
"""

import os
import re
import sys
import logging
import tempfile
import shutil
from pathlib import Path
import subprocess


import pyzipper  # pip install pyzipper

# ======================== НАСТРОЙКИ ========================

BUILDS_DIR = r"\\192.168.1.220\share\builds\iDБанк\master"
UPDATES_DIR = r"\\192.168.1.189\support\LocalUser\Public\updates\test"

VERSION_RE = re.compile(r"^\d+(\.\d+){3}$")
PASSWORD_PREFIX = "UPD"

LOG_FILE = Path(__file__).with_name("archive_build.log")

# ======================== ЛОГИРОВАНИЕ ========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("archive_build")


# ======================== ВСПОМОГАТЕЛЬНЫЕ ========================

def version_key(name: str):
    """'1.9.185.0' -> (1, 9, 185, 0) для корректного сравнения."""
    return tuple(int(p) for p in name.split("."))


def find_latest_version(builds_dir: str):
    if not os.path.isdir(builds_dir):
        raise FileNotFoundError(f"Каталог сборок недоступен: {builds_dir}")

    versions = [
        e for e in os.listdir(builds_dir)
        if VERSION_RE.match(e) and os.path.isdir(os.path.join(builds_dir, e))
    ]
    if not versions:
        return None, None

    latest = max(versions, key=version_key)
    return latest, os.path.join(builds_dir, latest)


def archive_name(version: str) -> str:
    return f"{version}.zip"


def password_for(version: str) -> str:
    return PASSWORD_PREFIX + version.replace(".", "")


def make_zip_zipcrypto(src_dir, dst_zip, password):
    # 7z a -tzip -mem=ZipCrypto -pПАРОЛЬ архив.zip содержимое
    log.info("Упаковка '%s' -> '%s' (ZipCrypto, пароль: %s)",
             src_dir, dst_zip, password)
    SEVEN_ZIP = r"C:\Program Files\7-Zip\7z.exe"
    if not os.path.isfile(SEVEN_ZIP):
        raise FileNotFoundError(f"7-Zip не найден: {SEVEN_ZIP}")
    cmd = [
        SEVEN_ZIP, "a", "-tzip", "-mem=ZipCrypto",
        f"-p{password}",
        dst_zip,
        os.path.join(src_dir, "*")  # или перечислите файлы
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    log.info("Архив создан: %s", dst_zip)


# ======================== ОСНОВНАЯ ЛОГИКА ========================

def main():
    log.info("=== Старт архивации ===")

    latest_version, latest_path = find_latest_version(BUILDS_DIR)
    if not latest_version:
        log.warning("В каталоге '%s' нет папок-версий.", BUILDS_DIR)
        return 1

    log.info("Последняя версия: %s (%s)", latest_version, latest_path)

    if not os.path.isdir(UPDATES_DIR):
        log.error("Каталог updates недоступен: %s", UPDATES_DIR)
        return 2

    target_zip = os.path.join(UPDATES_DIR, archive_name(latest_version))
    if os.path.isfile(target_zip):
        log.info("Архив уже существует, архивация не требуется: %s", target_zip)
        return 0

    pwd = password_for(latest_version)
    try:
        make_zip_zipcrypto(latest_path, target_zip, pwd)
    except Exception as e:
        log.exception("Ошибка при создании архива: %s", e)
        return 3

    log.info("=== Готово ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
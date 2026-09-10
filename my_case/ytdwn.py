import yt_dlp
import os


def download_youtube_video(url, output_path="./downloads"):
    """
    Скачивает видео с YouTube в наилучшем качестве 1080p/4K с аудио

    Args:
        url (str): Ссылка на видео YouTube
        output_path (str): Путь к папке для сохранения (по умолчанию ./downloads)
    """

    # Создаём папку, если её нет
    os.makedirs(output_path, exist_ok=True)

    # Настройки для загрузки
    ydl_opts = {
        # Формат: лучшее видео + лучшее аудио, объединённые в MP4
        'format': 'bestvideo+bestaudio/best',

        # Объединять видео и аудио с помощью FFmpeg
        'merge_output_format': 'mp4',

        # Путь для сохранения файла
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),

        # Прогресс-бар при загрузке
        'progress_hooks': [progress_hook],

        # Дополнительные настройки для стабильности
        'ignoreerrors': True,
        'no_warnings': False,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🚀 Начинаю загрузку: {url}")
            print(f"📁 Сохранение в: {output_path}")

            # Скачиваем видео
            info = ydl.extract_info(url, download=True)

            print(f"\n✅ Готово! Видео сохранено:")
            print(f"📹 Название: {info.get('title', 'Неизвестно')}")
            print(f"📏 Разрешение: {info.get('height', 'N/A')}p")
            print(f"📁 Путь: {output_path}")

    except Exception as e:
        print(f"❌ Ошибка при загрузке: {e}")


def progress_hook(d):
    """Отображает прогресс загрузки"""
    if d['status'] == 'downloading':
        # Показываем прогресс, если есть
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            print(f"\r⏳ Загрузка: {percent:.1f}%", end='')
    elif d['status'] == 'finished':
        print("\n✅ Файл загружен, обрабатываю...")


# ===== Использование =====

if __name__ == "__main__":
    # Вариант 1: Задать URL и папку вручную
    video_url = "https://www.youtube.com/watch?v=PV5sZ-57CcU"
    download_folder = r'E:\Torrent\MediaTorrent\YOUTUBE'  # Можно указать любой путь

    download_youtube_video(video_url, download_folder)

    # Вариант 2: Запросить у пользователя
    # url = input("Введите ссылку на YouTube: ")
    # folder = input("Введите путь для сохранения (Enter для ./downloads): ") or "./downloads"
    # download_youtube_video(url, folder)
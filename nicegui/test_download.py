from nicegui import ui, events
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_upload(e: events.UploadEventArguments):
    """Асинхронная обработка загруженного файла"""
    file_path = os.path.join(UPLOAD_DIR, e.file.name)
    await e.file.save(file_path)  # 👈 ОБЯЗАТЕЛЬНО await
    ui.notify(f'Файл "{e.file.name}" сохранён в {UPLOAD_DIR}!')

ui.upload(on_upload=handle_upload, auto_upload=True).classes('max-w-full')

ui.run()
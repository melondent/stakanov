from files.models import FileInfo
from datetime import datetime
from django.utils.timezone import make_aware

class DatabaseSaver:
    def __init__(self, logger):
        self.logger = logger

    def save_to_db(self, data, run_id):
        for file_info in data:
            try:
                created_at = None
                modified_at = None

                if file_info['created']:
                    created_at = datetime.strptime(file_info['created'], "%Y-%m-%d %H:%M:%S")
                    created_at = make_aware(created_at)

                if file_info['modified']:
                    modified_at = datetime.strptime(file_info['modified'], "%Y-%m-%d %H:%M:%S")
                    modified_at = make_aware(modified_at)
                
                FileInfo.objects.create(
                    name=file_info['name'],
                    path=file_info['file_path'],
                    size=file_info['size'],
                    extension=file_info['extension'],
                    created_at=created_at,
                    modified_at=modified_at,
                    width=file_info.get('width', None),
                    height=file_info.get('height', None),
                    area=file_info.get('area', None),
                    dpi=file_info.get('dpi', None),
                    exif_data=str(file_info.get('exif', None)),
                    pages=file_info.get('pages', None),
                    format=file_info.get('format', None),
                    orientation=file_info.get('orientation', None),
                    run_id=run_id
                )
            except Exception as e:
                self.logger.log_exception(f"Ошибка при сохранении файла {file_info.get('name', 'unknown')}: {str(e)}")

from files.models import FileInfo
from datetime import datetime
from django.utils.timezone import make_aware

class DatabaseSaver:
    """Сlass to save file information into a database.

    Attributes:
        logger (Logger): A logger instance for logging exceptions during database operations.
    """
    def __init__(self, logger):
        """Initializes the DatabaseSaver with a logger instance.

        Args:
            logger (Logger): A logger for capturing exceptions and other logs.
        """
        self.logger = logger

    def save_to_db(self, data, run_id):
        """Saves a list of file information to the database.

        Args:
            data (list): A list of dictionaries, where each dictionary contains metadata about a file.
            run_id (int): An identifier for the batch operation or run.

        FileInfo Fields Saved:
            - name (str): File name.
            - path (str): Full path to the file.
            - size (int): File size in bytes.
            - extension (str): File extension (e.g., .txt, .pdf).
            - created_at (datetime): Aware datetime when the file was created.
            - modified_at (datetime): Aware datetime when the file was last modified.
            - width (int, optional): Width of the file (e.g., image/video).
            - height (int, optional): Height of the file (e.g., image/video).
            - area (int, optional): Area of the file content (if applicable).
            - dpi (int, optional): DPI (dots per inch) for images.
            - exif_data (str, optional): EXIF metadata for images.
            - pages (int, optional): Number of pages (for documents like PDFs).
            - format (str, optional): Format or standard (e.g., A4, A3 for documents).
            - orientation (str, optional): Orientation of the file (portrait or landscape).
            - run_id (int): Identifier for the processing run.
        """
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

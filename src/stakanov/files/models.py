from django.db import models
from django.utils.timezone import now

class FileInfo(models.Model):
    """
    A model that stores information about files including metadata such as 
    file name, size, extension, and additional properties like image dimensions, 
    PDF pages, and EXIF data.
    
    Attributes:
        run_id (str): A unique identifier for the run that collected this file's information.
        name (str): The name of the file.
        path (str): The full path where the file is located.
        size (int): The size of the file in bytes.
        extension (str): The file's extension (e.g., '.jpg', '.pdf', etc.).
        created_at (datetime): The creation date and time of the file.
        modified_at (datetime): The last modified date and time of the file.
        width (int, optional): The width of the image if the file is an image (in pixels).
        height (int, optional): The height of the image if the file is an image (in pixels).
        area (int, optional): The area of the image if it's an image, calculated as width * height (in square pixels).
        dpi (int, optional): The DPI (dots per inch) of the image if applicable.
        exif_data (str, optional): The EXIF data for images, stored as a JSON string.
        pages (int, optional): The number of pages in the file if it is a document (e.g., PDF).
        format (str, optional): The format of the file, such as 'text/plain', 'image/jpeg', etc.
        orientation (str, optional): The orientation of the image, such as 'landscape' or 'portrait'.
    """
    run_id = models.CharField(max_length=36, null=True, blank=True)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    size = models.BigIntegerField()
    extension = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=now)
    modified_at = models.DateTimeField(default=now)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    dpi = models.IntegerField(null=True, blank=True)
    exif_data = models.TextField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=50, null=True, blank=True)
    orientation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        """
        Returns the name of the file as a string representation.

        Returns:
            str: The name of the file.
        """
        return self.name

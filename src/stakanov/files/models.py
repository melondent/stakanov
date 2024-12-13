from django.db import models

class FileInfo(models.Model):
    run_id = models.CharField(max_length=36, null=True, blank=True)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    size = models.BigIntegerField()
    extension = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    dpi = models.IntegerField(null=True, blank=True)
    exif_data = models.TextField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=50, null=True, blank=True)
    orientation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

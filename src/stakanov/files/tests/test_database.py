from django.test import TestCase
from files.models import FileInfo
import uuid
from django.utils.timezone import now
import os

class FileInfoModelTestCase(TestCase):
    """A test case for the FileInfo model."""
    def setUp(self):
        """Set up a test FileInfo instance for use in test methods."""
        self.file_info = FileInfo.objects.create(
            run_id=str(uuid.uuid4()),
            name="test_file.txt",
            path=os.getcwd(),
            size=2048,
            extension="txt",
            created_at=now(), 
            modified_at=now(),
            width=800,
            height=600,
            area=480000,
            dpi=300,
            exif_data="{}",
            pages=1,
            format="text/plain",
            orientation="landscape"
        )

    def test_file_info_creation(self):
        """Test the creation of a FileInfo instance."""
        self.assertEqual(FileInfo.objects.count(), 1)
        self.assertEqual(self.file_info.name, "test_file.txt")
        self.assertEqual(self.file_info.size, 2048)

    def test_file_info_str_method(self):
        """Test the string representation of a FileInfo instance."""
        self.assertEqual(str(self.file_info), "test_file.txt")

    def test_file_info_field_defaults(self):
        """Test that fields not explicitly set use their default values."""
        file_info = FileInfo.objects.create(
            name="test_file.jpg",
            path=os.getcwd(),
            size=1024,
            extension="jpg",
            created_at=now(), 
            modified_at=now(),
        )
        self.assertIsNone(file_info.run_id)
        self.assertIsNone(file_info.width)
        self.assertIsNone(file_info.height)

    def test_file_info_update(self):
        """Test updating a FileInfo instance and saving the changes."""
        self.file_info.name = "updated_file.txt"
        self.file_info.size = 4096
        self.file_info.save()
        
        updated_file = FileInfo.objects.get(id=self.file_info.id)
        self.assertEqual(updated_file.name, "updated_file.txt")
        self.assertEqual(updated_file.size, 4096)

    def test_file_info_deletion(self):
        """Test deleting a FileInfo instance."""
        self.file_info.delete()
        self.assertEqual(FileInfo.objects.count(), 0)

    def test_file_info_filtering(self):
        """Test filtering FileInfo instances based on a field value."""
        FileInfo.objects.create(
            name="test_file.png",
            path=os.getcwd(),
            size=5120,
            extension="png",
            created_at=now(), 
            modified_at=now(),
        )

        txt_files = FileInfo.objects.filter(extension="txt")
        self.assertEqual(txt_files.count(), 1)
        self.assertEqual(txt_files.first().name, "test_file.txt")

    def test_file_info_calculated_field(self):
        """Test that calculated fields, such as 'area' for image, have the
        correct values."""
        self.assertEqual(self.file_info.area, 480000)

    def test_file_info_null_values(self):
        """Test the handling of null values for optional fields."""
        file_info = FileInfo.objects.create(
            name="empty_file",
            path=os.getcwd(),
            size=0,
            extension="bin",
            created_at=now(), 
            modified_at=now(),
        )
        self.assertIsNone(file_info.width)
        self.assertIsNone(file_info.height)
        self.assertEqual(file_info.size, 0)

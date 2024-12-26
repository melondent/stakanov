from django.test import TestCase, Client
from django.urls import reverse
from files.models import FileInfo
import os
import uuid

class IndexViewTestCase(TestCase):
    """Test cases for the index page."""
    def setUp(self):
        """Set up the test client for sending requests to the views."""
        self.client = Client()

    def test_get_index(self):
        """Test the GET request to the index view.

        Verifies that the index page is rendered correctly with the
        expected context.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/index.html')
        self.assertIn('total_size', response.context)

    def test_post_index_without_folder(self):
        """Test a POST request without a folder parameter.

        Verifies that an appropriate error message is returned as JSON.
        """
        response = self.client.post(reverse('index'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Путь к папке не указан"}
        )

    def test_post_index_with_invalid_folder(self):
        """Test a POST request with an invalid folder path.

        Verifies that an appropriate error message is returned as JSON.
        """
        response = self.client.post(reverse('index'), data={'folder': '/invalid/path'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Папка не найдена )-:"}
        )

    def test_post_index_with_valid_folder(self):
        """Test a POST request with a valid folder path.

        Verifies that the response contains the expected JSON structure.
        """
        valid_folder = os.getcwd()
        with self.settings(INSTALLED_APPS=['collect.stakanov_logic']):
            response = self.client.post(reverse('index'), data={'folder': valid_folder})
            self.assertEqual(response.status_code, 200)
            self.assertIn("status", response.json())
            self.assertIn("message", response.json())

class ExtensionViewTestCase(TestCase):
    """Test cases for the extension page."""
    def setUp(self):
        """Set up the test client and initialize test data."""
        self.client = Client()

    def test_get_extension_without_run_id(self):
        """Set up the test client and initialize test data."""
        response = self.client.get(reverse('extension'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/error.html')
        self.assertIn("error", response.context)

    def test_get_extension_with_run_id(self):
        """Test the GET request to the extension view with a valid run ID.

        Verifies that the extension statistics are rendered correctly in
        the template.
        """
        run_id = str(uuid.uuid4())
        FileInfo.objects.create(name="test_file.txt", size=1024, extension="txt", run_id=run_id)
        session = self.client.session
        session['last_run_id'] = run_id
        session.save()

        response = self.client.get(reverse('extension'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/extension.html')
        self.assertIn('extension_stats', response.context)

class PdfViewTestCase(TestCase):
    """Test cases for the pdf page."""
    def setUp(self):
        """Set up the test client and initialize test data."""
        self.client = Client()

    def test_get_pdf_without_run_id(self):
        """Test the GET request to the PDF view without a valid run ID.

        Verifies that an error template is rendered with the appropriate
        context.
        """
        response = self.client.get(reverse('pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/error.html')
        self.assertIn("error", response.context)

    def test_get_pdf_with_run_id(self):
        """Test the GET request to the PDF view with a valid run ID.

        Verifies that the top documents are rendered correctly in the
        template.
        """
        run_id = str(uuid.uuid4())
        FileInfo.objects.create(name="test_doc.pdf", size=2048, pages=10, run_id=run_id)
        session = self.client.session
        session['last_run_id'] = run_id
        session.save()

        response = self.client.get(reverse('pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/pdf.html')
        self.assertIn('top_documents', response.context)

class SizeViewTestCase(TestCase):
    """Test cases for the size page."""
    def setUp(self):
        """Set up the test client and initialize test data."""
        self.client = Client()

    def test_get_size_without_run_id(self):
        """Test the GET request to the size view without a valid run ID.

        Verifies that an error template is rendered with the appropriate
        context.
        """
        response = self.client.get(reverse('size'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/error.html')
        self.assertIn("error", response.context)

    def test_get_size_with_run_id(self):
        """Test the GET request to the size view with a valid run ID.

        Verifies that the top files by size are rendered correctly in
        the template.
        """
        run_id = str(uuid.uuid4())
        FileInfo.objects.create(name="large_file.bin", size=1048576, run_id=run_id)
        session = self.client.session
        session['last_run_id'] = run_id
        session.save()

        response = self.client.get(reverse('size'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/size.html')
        self.assertIn('top_files', response.context)

class ImageViewTestCase(TestCase):
    """Test cases for the image page."""
    def setUp(self):
        """Set up the test client and initialize test data."""
        self.client = Client()

    def test_get_image_without_run_id(self):
        """Test the GET request to the image view without a valid run ID.

        Verifies that an error template is rendered with the appropriate
        context.
        """
        response = self.client.get(reverse('image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/error.html')
        self.assertIn("error", response.context)

    def test_get_image_with_run_id(self):
        """Test the GET request to the image view with a valid run ID.

        Verifies that the top images are rendered correctly in the
        template.
        """
        run_id = str(uuid.uuid4())
        FileInfo.objects.create(name="image.jpg", size=512, area=1024, run_id=run_id)
        session = self.client.session
        session['last_run_id'] = run_id
        session.save()

        response = self.client.get(reverse('image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/image.html')
        self.assertIn('top_images', response.context)

class ErrorViewTestCase(TestCase):
    """Test cases for the error page."""
    def setUp(self):
        """Set up the test client and initialize test data."""
        self.client = Client()

    def test_get_error(self):
        """Test the GET request to the error view.

        Verifies that the error page is rendered correctly with the
        expected context.
        """
        response = self.client.get(reverse('error'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/error.html')
        self.assertIn('total_size', response.context)

from django.test import TestCase
from collect.stakanov_logic import Indiana, GeneralResearcher, Logger
import tempfile
import os

class IndianaTestCase(TestCase):
    """A test case for validating the functionality of the Indiana class."""
    def setUp(self):
        """Set up a temporary directory and file for testing.

        Initializes an instance of the Indiana class with the temporary
        directory as its search path and prepares a GeneralResearcher
        instance for supplementary operations.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = tempfile.NamedTemporaryFile(dir=self.temp_dir.name, delete=False)
        self.temp_file.close()
        self.indiana = Indiana(path=self.temp_dir.name, output_file="test_output.csv")
        self.general_researcher = GeneralResearcher()

    def test_find_loot(self):
        """Test the find_loot method to ensure it discovers files in the
        specified directory."""
        self.indiana.find_loot()
        self.assertGreater(len(self.indiana.data), 0)
        self.assertEqual(self.indiana.data[0]['file_path'], self.temp_file.name)
    
    def test_save_results(self):
        """Test the save_results method to ensure it writes the discovered
        files data to a CSV file.

        Verifies the existence of the output CSV file after the
        save_results method is called.
        """
        self.indiana.find_loot()
        self.indiana.save_results()
        self.assertTrue(os.path.exists("test_output.csv"))

    def tearDown(self):
        """Clean up the temporary directory and any generated files after tests
        complete."""
        self.temp_dir.cleanup()
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")
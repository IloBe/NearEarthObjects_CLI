"""Check that the data files exist and are readable, nonempty, and well-formatted.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_data_files

These tests should pass on the starter code.
"""

###############
# Imports
###############
import collections
import csv
import json
import os
import unittest

# import own files
import config as cfg


###############
# Coding
###############

class TestDataFiles(unittest.TestCase):
    def setUp(self):
        self.neo_file = cfg.DATA_ROOT / 'neos.csv'
        self.cad_file = cfg.DATA_ROOT / 'cad.json'

    def test_data_files_exist(self):
        self.assertTrue(self.neo_file.exists())
        self.assertTrue(self.cad_file.exists())

    def test_data_files_are_readable(self):
        self.assertTrue(os.access(self.neo_file, os.R_OK))
        self.assertTrue(os.access(self.cad_file, os.R_OK))

    def test_data_files_are_not_empty(self):
        try:
            self.assertTrue(
                self.neo_file.stat().st_size > 0,
                "Empty NEO file.")
            self.assertTrue(
                self.cad_file.stat().st_size > 0,
                "Empty CAD file.")
        except OSError:
            self.fail("Unexpected OSError.")

    def test_data_files_are_well_formatted(self):
        """ Checks if the data is welll formatted according CSV or JSON. """
        # Check that the NEO data is CSV-formatted.
        try:
            with self.neo_file.open() as csv_file:
                # Consume the entire sequence into length-0 deque.
                collections.deque(csv.reader(csv_file), maxlen=0)
        except csv.Error as err:
            raise self.failureException(
                f"{self.neo_file!r} is not a well-formated CSV.") from err

        # Check that the CAD data is JSON-formatted.
        try:
            with self.cad_file.open() as json_file:
                json.load(json_file)
            json.loads(self.cad_file.read_text())
        except json.JSONDecodeError as err:
            raise self.failureException(
                f"{self.cad_file!r} is not a valid JSON document.") from err


if __name__ == '__main__':
    unittest.main()

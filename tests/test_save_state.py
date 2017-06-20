import sqlite3
import unittest
from dojo_classes.Dojo import Dojo


class TestSaveState(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_save_state(self):
        self.offices = self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.living_spaces = self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")
        self.dojo.add_person("Jackson Brown", "Staff")
        self.dojo.add_person("Jennifer Hopkins", "Fellow", "Y")
        self.dojo.save_state("test_db")
        self.assertTrue(sqlite3.connect('ExternalData/test_db.db'), msg="Can't connect to saved db")

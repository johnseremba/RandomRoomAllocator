import unittest
from dojo_classes.Dojo import Dojo
from dojo_classes.Room import LivingSpace, Office


class TestLoadData(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_count_num_of_entries(self):
        self.dojo.load_state("dojo")
        self.assertEqual(len(self.dojo.all_people), 5, msg="Loaded persons should be 5")
        self.assertEqual(len(self.dojo.all_rooms), 6, msg="Should load 6 rooms")
        self.assertEqual(len([room for room in self.dojo.all_rooms if isinstance(room, Office)]), 3,
                         msg="Loaded Office instances should be 3")
        self.assertEqual(len([room for room in self.dojo.all_rooms if isinstance(room, LivingSpace)]), 3,
                         msg="Loaded Living Space instances should be 3")

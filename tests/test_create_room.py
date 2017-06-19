import unittest
from dojo_classes.Dojo import Dojo
from dojo_classes.Room import LivingSpace, Office


class TestCreateRoom (unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_create_room_successfully(self):
        new_room = self.dojo.create_room("office", "Blue")
        new_room_count = len(new_room)
        self.assertEqual(new_room_count, 1, msg="Total rooms should be 1")

    def test_create_room_invalid_chars(self):
        new_room = self.dojo.create_room("office", "Y3ll@!-=")
        new_room_count = len(new_room)
        self.assertEqual(new_room_count, 0, msg="Room name contains invalid chars shouldn't be created")

    def test_invalid_room_type(self):
        new_room = self.dojo.create_room("some_room_type", "Blue")
        new_room_count = len(new_room)
        self.assertEqual(new_room_count, 0, msg="Room shouldn't be created")

    def test_create_many_rooms(self):
        new_rooms = self.dojo.create_room("office", "Purple", "Black", "Brown")
        new_room_count = len([office for office in new_rooms if isinstance(office, Office)])
        self.assertEqual(new_room_count, 3, msg="Created offices should be 3")

    def test_create_living_space(self):
        new_room = self.dojo.create_room("living_space", "Ruby")
        new_room_count = len([living_space for living_space in new_room if isinstance(living_space, LivingSpace)])
        self.assertEqual(new_room_count, 1, msg="Total rooms should be 1")

    def test_create_many_living_space(self):
        new_rooms = self.dojo.create_room("living_space", "Ruby", "Shell", "Python")
        new_room_count = len([living_space for living_space in new_rooms if isinstance(living_space, LivingSpace)])
        self.assertEqual(new_room_count, 3, msg="Total living spaces should be 3")

    def test_create_duplicate_rooms(self):
        new_room_1 = self.dojo.create_room("office", "Blue")
        new_room_2 = self.dojo.create_room("office", "Blue")
        new_rooms = new_room_1 + new_room_2
        new_room_count = len(new_rooms)
        self.assertEqual(new_room_count, 1,
                         msg="Should not create two or more rooms with the same names")

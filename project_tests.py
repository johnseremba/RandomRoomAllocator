import unittest
from RandomRoomAllocator import Dojo


class TestCreateRoom (unittest.TestCase):
    def setUp(self):
        self.my_dojo = Dojo()

    def test_create_room_successfully(self):
        initial_room_count = len(self.my_dojo.all_rooms)
        blue_office = self.my_dojo.create_room("Blue", "office")
        self.assertTrue(blue_office)
        new_room_count = len(self.my_dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1, msg="Total rooms should be 1")
        blue_office.assertIsInstance(self.my_dojo.Office, "Instance should be of type Office")

    def test_create_many_rooms(self):
        initial_room_count = len(self.my_dojo.all_rooms)
        offices = self.my_dojo.create_room("office", "Purple", "Black", "Brown")
        self.assetTrue(offices)
        new_room_count = len(self.my_dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3, msg="Created rooms should be 3")

    def test_create_living_space(self):
        initial_room_count = len(self.my_dojo.all_rooms)
        living_space = self.my_dojo.create_room("Yellow", "living_space")
        self.assetTrue(living_space)
        new_room_count = len(self.my_dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1, msg="Created living space should be 1")
        living_space.assertIsInstance(self.my_dojo.LivingSpace, msg="Room should be an instance of Living Space")




import unittest
from RandomRoomAllocator import Dojo


class TestCreateRoom (unittest.TestCase):
    def setUp(self):
        self.my_dojo = Dojo()

    def test_create_room_successfully(self):
        initial_room_count = len(self.my_dojo.all_rooms)
        blue_office = self.my_dojo.create_room("office", "Blue")
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
        living_space = self.my_dojo.create_room("living_space", "Yellow")
        self.assetTrue(living_space)
        new_room_count = len(self.my_dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1, msg="Created living space should be 1")
        living_space.assertIsInstance(self.my_dojo.LivingSpace, msg="Room should be an instance of Living Space")


class TestAllocateRoom(unittest.TestCase):
    def SetUp(self):
        self.my_dojo = Dojo()
        self.offices = self.my_dojo.create_room("office", "Purple", "Black", "Brown")
        self.living_space = self.my_dojo.create_room("office", "Yellow", "Orange", "Pink")

    def test_add_person(self):
        self.my_dojo.add_person("Neil Armstrong", "Staff")
        self.my_dojo.add_person("Nelly Armweek", "Fellow", "Y")
        self.my_dojo.add_person("Johnson Jones", "Fellow")
        all_people = len(self.my_dojo.all_people)
        self.assertEqual(all_people, 3, msg="all_people should be equal to 3")
        for person in self.my_dojo.all_people:
            if person is self.my_dojo.Staff:
                person.assertTrue(person.Office, msg="Staff member should be assigned an office")
                person.assertFalse(person.LivingSpace, msg="Staff member shoulld not have a living space")
                continue
            if person is self.my_dojo.Fellow:
                person.assertTrue(person.Office, msg="Fellow should be assigned an office")
                if person.wants_accomodation:
                    person.assertTrue(person.LivingSpace,
                                      msg="Fellow wants a room. Therefore he/she must be assigned a living space")
                else:
                    person.assertFalse(person.LivingSpace, msg="Fellow should not be assigned a living space.")

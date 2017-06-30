import unittest
from dojo_classes.Dojo import Dojo


class TestReallocation(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_reallocate_office(self):
        current_office = self.dojo.create_room("office", "Blue")[0]
        person = self.dojo.add_person("Dominic Sanders", "Fellow")
        new_office = self.dojo.create_room("office", "Black")[0]

        self.dojo.reallocate_person("FW1", "Black")
        self.assertTrue(person in new_office.occupants and person not in current_office.occupants,
                        msg="Person should be an occupant of the new room, and removed from the previous room")

    def test_reallocate_same_office(self):
        self.dojo.create_room("office", "Blue")
        self.dojo.add_person("Johnson Brown", "Staff")
        self.assertFalse(self.dojo.reallocate_person("ST1", "Blue"), msg="Can't reallocate person to same office")

    def test_no_current_office(self):
        self.dojo.add_person("Dominic Sanders", "Fellow")
        self.dojo.create_room("office", "Black")
        self.assertFalse(self.dojo.reallocate_person("FW1", "Black"),
                         msg="Can't reallocate person without current office")

    def test_reallocate_nonexistent_office(self):
        self.assertFalse(self.dojo.reallocate_person("FW1", "Outopia"), msg="Can't reallocate to nonexistent office")

    def test_nonexistent_person(self):
        self.assertFalse(self.dojo.reallocate_person("FW2", "Black"), msg="Can't reallocate nonexistent person")

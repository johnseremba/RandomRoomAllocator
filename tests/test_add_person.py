import unittest
from dojo_classes.Dojo import Dojo
from dojo_classes.Person import Fellow, Staff


class TestAddPerson(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_add_person_fellow(self):
        new_person = self.dojo.add_person("Dominic Waters", "Fellow")
        self.assertTrue(isinstance(new_person, Fellow), msg="Fellow object should be created")

    def test_add_person_fellow_with_accommodation(self):
        new_person = self.dojo.add_person("Dominic Sanders", "Fellow", "Y")
        self.assertTrue(new_person.opt_in, msg="The fellow chose to opt in. opt_in should be True")

    def test_add_person_staff(self):
        new_person = self.dojo.add_person("Leih Reileh", "Staff")
        self.assertTrue(isinstance(new_person, Staff), msg="Should create staff object!")

    def test_staff_with_accommodation(self):
        living_space = self.dojo.create_room("living_space", "Brown")[0]
        new_staff = self.dojo.add_person("Leih Reileh", "Staff", "Y")
        self.assertFalse(new_staff in living_space.occupants, msg="Staff shouldn't be assigned accommodation")

    def test_add_person_invalid_person_type(self):
        new_person = self.dojo.add_person("Sanders Dominic", "some_person_type")
        self.assertTrue(new_person is None, "Person type should either be Fellow or Staff")

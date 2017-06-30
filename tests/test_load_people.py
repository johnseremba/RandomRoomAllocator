import unittest
from dojo_classes.Dojo import Dojo
from dojo_classes.Person import Fellow, Staff


class LoadPeopleFromFile(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.offices = self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.living_spaces = self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")
        self.dojo.load_people()
        self.all_people = self.dojo.all_people

    def test_count_people_added(self):
        self.assertEqual(len(self.all_people), 7, msg="Added people should be 7")

    def test_count_instances(self):
        added_staff = len([person for person in self.all_people if isinstance(person, Staff)])
        added_fellows = len([person for person in self.all_people if isinstance(person, Fellow)])

        self.assertEqual(added_staff, 3, msg="A total of 3 staff members should be added")
        self.assertEqual(added_fellows, 4, msg="A total of 4 fellows should be added")

    def test_office_allocations(self):
        office_list = self.offices
        for person in self.dojo.all_people:
            allocated = False
            for office in office_list:
                for occupant in office.occupants:
                    if occupant.person_name == person.person_name:
                        allocated = True
                        break
            self.assertTrue(allocated, msg="Person should be allocated an office after loading data")

    def test_living_space_allocations(self):
        living_space_list = self.living_spaces
        for person in [person for person in self.all_people if isinstance(person, Fellow) and person.opt_in]:
            allocated = False
            for living_space in living_space_list:
                for occupant in living_space.occupants:
                    if occupant.person_name == person.person_name:
                        allocated = True
                        break
            self.assertTrue(allocated, msg="Fellow with argument Y should be allocated an office")

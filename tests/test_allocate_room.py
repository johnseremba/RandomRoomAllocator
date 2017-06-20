import unittest
from dojo_classes.Dojo import Dojo
import os


class TestAllocateRoom(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_allocate_person_staff(self):
        office_list = self.dojo.create_room("office", "Blue", "Black")
        staff = self.dojo.add_person("Neil Armstrong", "Staff")
        allocated = False
        for office in office_list:
            for occupant in office.occupants:
                if occupant.person_name == staff.person_name:
                    allocated = True
                    break
        self.assertTrue(allocated, msg="Staff member should be assigned an office")

    def test_allocate_office_fellow(self):
        office = self.dojo.create_room("office", "Blue")
        staff = self.dojo.add_person("Dominic Waters", "Fellow")
        allocated = False
        if office[0].occupants[0].person_name == staff.person_name:
            allocated = True
        self.assertTrue(allocated, msg="Fellow should be assigned an office")

    def test_allocate_living_space_fellow(self):
        living_space = self.dojo.create_room("living_space", "Orange")
        fellow = self.dojo.add_person("Simon Peterson", "Fellow", "Y")
        allocated = False
        if living_space[0].occupants[0].person_name == fellow.person_name:
            allocated = True
        self.assertTrue(allocated, msg="Fellow that chose to opt in should be assigned a Living Space")

    def test_staff_with_living_space(self):
        living_space = self.dojo.create_room("living_space", "Orange")
        self.dojo.add_person("Dominic Walters", "Staff", "Y")
        count_occupants = len(living_space[0].occupants)
        self.assertEqual(count_occupants, 0, msg="Staff members should never be allocated living space")

    def test_print_occupants_allocations(self):
        living_spaces_list = self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")
        office_list = self.dojo.create_room("office", "Blue", "Black")
        self.dojo.add_person("Neil Jones", "Staff")
        self.dojo.add_person("Mike Peterson", "Fellow", "Y")

        rooms = living_spaces_list + office_list
        occupied_rooms = [room for room in rooms if len(room.occupants) > 0]

        for room in occupied_rooms:
            self.assertTrue(self.dojo.print_room(room.room_name), msg="Room should have occupants")

    def test_allocations_nonexistent(self):
        self.assertFalse(self.dojo.print_room("Outopia"), msg="Room doesn't exist")

    def test_allocations_not_occupied(self):
        self.dojo.create_room("office", "Blue")
        self.assertFalse(self.dojo.print_room("Blue"), msg="Room should not have occupants")

    def test_allocations(self):  # pragma: no cover
        self.dojo.create_room("office", "Blue")
        self.dojo.add_person("Neil Jones", "Staff")
        self.dojo.print_allocations("allocations_tests")
        my_file = open(os.path.join(os.path.dirname(__file__), "tests/ExternalData/allocations_tests.txt")).read()
        self.assertTrue("BLUE" in my_file, msg="The room Blue should be printed to the file")
        self.assertTrue("Neil Jones" in my_file, msg="Neil Jones should be printed to the file")

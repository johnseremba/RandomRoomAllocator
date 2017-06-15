import sqlite3
import unittest

from dojo_classes.Dojo import Dojo
from dojo_classes.Person import Fellow, Staff
from dojo_classes.Room import LivingSpace, Office


class TestCreateRoom (unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_create_room_successfully(self):
        initial_room_count = len(self.dojo.all_rooms)
        self.dojo.create_room("office", "Blue", "Green,")
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1, msg="Total rooms should be 1")

    def test_invalid_room_type(self):
        initial_room_count = len(self.dojo.all_rooms)
        self.dojo.create_room("officez", "Blue", "Green,")
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 0, msg="Room shouldn't be created")

    def test_create_many_rooms(self):
        initial_room_count = len(self.dojo.all_rooms)
        self.dojo.create_room("office", "Purple", "Black", "Brown")
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 3, msg="Created rooms should be 3")
        self.assertEqual(len([x for x in self.dojo.all_rooms
                              if isinstance(x, Office)]), 3, msg="Created offices should be 4")

    def test_create_living_space(self):
        initial_room_count = len(self.dojo.all_rooms)
        self.dojo.create_room("living_space", "Yellow")
        new_room_count = len(self.dojo.all_rooms)
        self.assertEqual(new_room_count - initial_room_count, 1, msg="Created living space should be 1")

    def test_create_duplicate_rooms(self):
        initial_room_count = len(self.dojo.all_rooms)
        new_rooms = self.dojo.create_room("Office", "Blue", "Blue")
        self.assertTrue(new_rooms[0])
        self.assertEqual(len(new_rooms) - initial_room_count, 1,
                         msg="Should not create two or more rooms with the same names")


class TestAddPerson(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()

    def test_add_person_fellow(self):
        initial_person_count = len(self.dojo.all_people)
        new_person = self.dojo.add_person("Dominic Waters", "Fellow")
        self.assertTrue(new_person, msg="Person not created!")
        self.assertIsInstance(new_person, Fellow, msg="Person created should be of instance Fellow")
        self.assertEqual(len(self.dojo.all_people) - initial_person_count, 1,
                         msg="Created person should be added to all_people")

    def test_add_person_staff(self):
        initial_person_count = len(self.dojo.all_people)
        new_person = self.dojo.add_person("Leih Reileh", "Staff")
        self.assertTrue(new_person, msg="Person not created!")
        self.assertIsInstance(new_person, Staff, msg="Person created should be of instance Staff")
        self.assertEqual(len(self.dojo.all_people) - initial_person_count, 1,
                         msg="Created person should be added to all_people")

    def test_add_person_fellow_with_accommodation(self):
        new_person = self.dojo.add_person("Dominic Sanders", "Fellow", "Y")
        self.assertTrue(new_person, msg="Person not created!")
        self.assertTrue(new_person.opt_in, msg="The fellow chose to opt in. opt_in should be True")

    def test_add_person_wrong_person_type(self):
        new_person = self.dojo.add_person("Sanders Dominic", "Someone")
        self.assertFalse(new_person, "Person type should either be Fellow or Staff")


class TestAllocateRoom(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")

    def test_allocate_person_staff(self):
        my_staff = self.dojo.add_person("Neil Armstrong", "Staff")
        self.assertTrue(my_staff, msg="Staff member not created!")
        office_list = [office for office in self.dojo.all_rooms if isinstance(office, Office)]
        allocated = False
        for office in office_list:
            for occupant in office.occupants:
                if occupant.person_name == "Neil Armstrong":
                    allocated = True
                    break
        self.assertTrue(allocated, msg="Staff member should be assigned an office")

    def test_allocate_office_fellow(self):
        self.dojo.add_person("Dominic Waters", "Fellow")
        office_list = [office for office in self.dojo.all_rooms if isinstance(office, Office)]
        allocated = False
        for office in office_list:
            for occupant in office.occupants:
                if occupant.person_name == "Dominic Waters":
                    allocated = True
                    break
        self.assertTrue(allocated, msg="Fellow should be assigned an office")

    def test_print_occupants_allocations(self):
        self.dojo.add_person("Neil Jones", "Staff")
        self.dojo.add_person("Mike Peterson", "Fellow", "Y")
        occupied_rooms = [room for room in self.dojo.all_rooms if len(room.occupants) > 0]
        not_occupied_rooms = [room for room in self.dojo.all_rooms if len(room.occupants) < 1]

        for room in occupied_rooms:
            self.assertTrue(self.dojo.print_room(room.room_name), msg="Room should have occupants")

        for room in not_occupied_rooms:
            self.assertFalse(self.dojo.print_room(room.room_name), msg="Room should not have occupants")

        self.assertFalse(self.dojo.print_room("Outopia"), msg="Room doesn't exist")

    def test_allocate_living_space_fellow(self):
        self.dojo.add_person("Simon Peterson", "Fellow", "Y")
        living_space_list = [living_space for living_space in self.dojo.all_rooms if isinstance(living_space, LivingSpace)]
        allocated = False
        for living_space in living_space_list:
            for occupant in living_space.occupants:
                if occupant.person_name == "Simon Peterson":
                    allocated = True
                    break
        self.assertTrue(allocated, msg="Fellow that chose to opt in should be assigned a Living Space")

    def test_staff_with_living_space(self):
        new_staff = self.dojo.add_person("Dominic Walters", "Staff", "Y")
        self.assertTrue(new_staff, "Should ignore accommodation parameter for staff")
        living_space_list = [living_space for living_space in self.dojo.all_rooms
                             if isinstance(living_space, LivingSpace) and new_staff in living_space.occupants]
        self.assertFalse(living_space_list, msg="Staff members should never be allocated living space")


class LoadPeopleFromFile(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")
        self.dojo.load_people()

    def test_count_people_added(self):
        self.assertEqual(len(self.dojo.all_people), 7, msg="Added people should be 7")

    def test_count_instances(self):
        self.assertEqual(len([person for person in self.dojo.all_people if isinstance(person, Staff)]), 3,
                         msg="A total of 3 staff members should be added")
        self.assertEqual(len([person for person in self.dojo.all_people if isinstance(person, Fellow)]), 4,
                         msg="A total of 4 fellows should be added")

    def test_office_allocations(self):
        office_list = [office for office in self.dojo.all_rooms if isinstance(office, Office)]
        for person in self.dojo.all_people:
            allocated = False
            for office in office_list:
                for occupant in office.occupants:
                    if occupant.person_name == person.person_name:
                        allocated = True
                        break
            self.assertTrue(allocated, msg="Person should be allocated an office after loading data")

    def test_living_space_allocations(self):
        living_space_list = [living_space for living_space in self.dojo.all_rooms
                             if isinstance(living_space, LivingSpace)]
        for person in [person for person in self.dojo.all_people if isinstance(person, Fellow) and person.opt_in]:
            allocated = False
            for living_space in living_space_list:
                for occupant in living_space.occupants:
                    if occupant.person_name == person.person_name:
                        allocated = True
                        break
            self.assertTrue(allocated, msg="Fellow with argument Y should be allocated an office")

    def test_allocations(self):
        self.dojo.print_allocations("allocations_tests")
        my_file = open("ExternalData/allocations_tests.txt")
        self.assertTrue(my_file, msg="Should output a .txt file")
        my_file.close()
        self.assertTrue(self.dojo.print_all_data(), msg="Should print all data")


class TestReallocation(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.person = self.dojo.add_person("Dominic Sanders", "Fellow", "Y")

    def test_rellocate_office(self):
        self.assertFalse(self.dojo.reallocate_person("FW1", "Outopia"), msg="Room doesn't exist")
        self.assertFalse(self.dojo.reallocate_person("FW2", "Black"), msg="Person doesn't exist")

        offices = [office for office in self.dojo.all_rooms
                          if isinstance(office, Office)]
        current_office = [office for office in offices if self.person in office.occupants][0]
        self.assertTrue(current_office, msg="Person should have a current office")
        self.dojo.reallocate_person("FW1", "Black")
        new_office = [office for office in self.dojo.all_rooms if isinstance(office, Office) and office.room_name == "Black"][0]
        self.assertTrue(self.person in new_office.occupants,
                        msg="Person should be an occupant of the new room")

        if current_office is not new_office:
            self.assertFalse(self.person in current_office.occupants,
                             msg="Person should be removed from the previous office")

        self.assertFalse(self.dojo.reallocate_person("FW1", "Black"), msg="Can't reallocate to same office")


class TestUnallocatedPeople(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", "Blue")
        self.dojo.create_room("living_space", "Orange")
        self.person = self.dojo.add_person("Dominic Sanders", "Fellow", "Y")
        self.person = self.dojo.add_person("Jennipher Hopkins", "Fellow", "Y")
        self.dojo.load_people()

    def test_unallocated(self):
        results = self.dojo.print_unallocated(None)
        un_staff = results[0]
        un_fellow = results[1]
        un_fellow_living = results[2]

        self.assertEqual(un_staff, 2, "2 Staff member should not be allocated offices")
        self.assertEqual(un_fellow, 1, "1 Fellows should not be allocated an office")
        self.assertEqual(un_fellow_living, 2, "2 Staff member should not be allocated living space")

    def test_print_unallocated(self):
        self.dojo.print_unallocated("un_allocated_tests")
        my_file = open("ExternalData/un_allocated_tests.txt")
        self.assertTrue(my_file, msg="Should output a .txt file")
        my_file.close()


class TestSaveState(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo()
        self.dojo.create_room("office", "Blue", "Black", "Brown")
        self.dojo.create_room("living_space", "Orange", "Yellow", "Purple")
        self.dojo.load_people()

    def test_save_state(self):
        self.dojo.save_state("test_db")
        self.assertTrue(sqlite3.connect('ExternalData/test_db.db'), msg="Can't connect to saved db")


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

if __name__ == '__main__':
    unittest.main()

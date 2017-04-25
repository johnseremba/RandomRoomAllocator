from RandomRoomAllocator.Room import Office
from RandomRoomAllocator.Room import LivingSpace
from random import randint

class Person:
    def __init__(self, person_name):
        self.person_name = person_name

    def allocate_office(self, person_name, rooms_list):
        available_offices = [room for room in rooms_list
                             if isinstance(room, Office) and (len(room.occupants) <= 6)]
        num_offices = len(available_offices)
        if num_offices > 0:
            office_to_assign = randint(0, num_offices)
            rooms_list[office_to_assign].occupants.append(self)
            print("%s has been allocated the office %s" % (person_name, rooms_list[office_to_assign].room_name))
        else:
            print("No Offices to assign")


class Staff(Person):
    def __init__(self, person_name, rooms_list):
        self.person_name = person_name
        self.allocate_office(self.person_name, rooms_list)


class Fellow(Person):
    def __init__(self, person_name, opt_in, rooms_list):
        self.person_name = person_name
        self.allocate_office(self.person_name, rooms_list)
        if opt_in:
            self.allocate_living_space(self.person_name, rooms_list)

    def allocate_living_space(self, person_name, rooms_list):
        available_living_spaces = [room for room in rooms_list
                                   if isinstance(room, LivingSpace) and (len(room.occupants) <= 4)]
        num_spaces = len(available_living_spaces)
        if num_spaces > 0:
            space_to_assign = randint(0, num_spaces)
            rooms_list[space_to_assign].occupants.append(self)
            print("%s has been allocated the Living Space %s" % (person_name, rooms_list[space_to_assign].room_name))
        else:
            print("No Living Space to assign")

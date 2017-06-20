from abc import ABCMeta
from random import SystemRandom

from dojo_classes.Room import Office, LivingSpace


class Person(metaclass=ABCMeta):
    def __init__(self, person_name, person_id):
        if isinstance(self, Person):
            raise NotImplementedError("You can't directly instantiate a Person object")

        new_name = person_name.split(" ")
        self.person_name = new_name[0].capitalize() + ' ' + new_name[1].capitalize()
        self.person_id = person_id

    def allocate_office(self, person_name, rooms_list):
        available_offices = [room for room in rooms_list
                             if isinstance(room, Office) and (len(room.occupants) < int(room.max_occupants))]
        num_offices = len(available_offices)
        if num_offices > 0:
            assigned_office = available_offices[SystemRandom().randrange(0, num_offices) - 1]
            assigned_office.occupants.append(self)
            print("%s has been allocated the office %s" % (person_name.partition(' ')[0], assigned_office.room_name))
        else:
            print("No Offices to assign")


class Staff(Person):
    def __init__(self, person_name, person_id):
        super().__init__(person_name, person_id)


class Fellow(Person):
    def __init__(self, person_name, opt_in, person_id):
        super().__init__(person_name, person_id)
        self.opt_in = opt_in

    def allocate_living_space(self, person_name, rooms_list):
        available_living_spaces = [room for room in rooms_list
                                   if isinstance(room, LivingSpace) and (len(room.occupants) < int(room.max_occupants))]
        num_spaces = len(available_living_spaces)
        if num_spaces > 0:
            assigned_living_space = available_living_spaces[SystemRandom().randrange(0, num_spaces) - 1]
            assigned_living_space.occupants.append(self)
            print("%s has been allocated the Living Space %s" %
                  (person_name.partition(' ')[0], assigned_living_space.room_name))
        else:
            print("No Living Space to assign")

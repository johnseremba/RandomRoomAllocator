"""Greeter.

Usage:
 Dojo.py create_room <room_type> <room_name> ...
 Dojo.py (-h | --help)

Options:
 -h --help     Show this screen.

"""

from RandomRoomAllocator.Room import *
from RandomRoomAllocator.Person import *

class Dojo:
    def __init__(self):
        self.dojo_name = "Kenya Dojo"
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_name):
        """
        Creates a new room basing on the room type, returns true if created successfully and false otherwise
        :param room_type: string
        :param room_name: string
        :return: True/False
        """
        if room_type == "office":
            for room in room_name:
                new_office = Office(room_name)
                if new_office:
                    self.all_rooms.append(new_office)
                else:
                    return False
            return True
        else:
            for room in room_name:
                new_livin_space = LivingSpace(room_name)
                if new_livin_space:
                    self.all_rooms.append(new_livin_space)
                else:
                    return False
            return True

    def add_person(self, person_name, person_type):
        if person_type == "Staff":
            return Staff(person_name)
        else:
            return Fellow(person_name)

# if __name__ == '__main__':
#    arguments = docopt(__doc__)

my_dojo = Dojo()
my_office = my_dojo.create_room("office", "Blue")
my_living = my_dojo.create_room("living", "Yellow")
my_person1 = my_dojo.create_person("Serry", "Fellow")
my_person2 = my_dojo.create_person("Johnz", "Staff")

print(my_person1)
print(my_person2)
#print(my_living.LivingSpace)

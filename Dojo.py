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

    def create_room(self, room_type, room_name):
        if room_type == "office":
            return Office(room_name)
        else:
            return LivingSpace(room_name)

    def add_person(self, person_name, person_type):
        if person_type == "Staff":
            return Staff(person_name)
        else:
            return Fellow(person_name)

# if __name__ == '__main__':
#    arguments = docopt(__doc__)
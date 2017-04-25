from RandomRoomAllocator.Room import *
from RandomRoomAllocator.Person import *


class Dojo:
    def __init__(self):
        self.dojo_name = "Kenya Dojo"
        self.all_rooms = []
        self.all_people = []

    def create_room(self, room_type, *room_name):
        """Usage: create_room <room_type> <room_name>..."""
        rooms_list = list(room_name)
        if room_type == "office":
            for room in rooms_list:
                new_office = Office(room)
                if new_office:
                    self.all_rooms.append(new_office)
                else:
                    return False
        else:
            for room in rooms_list:
                new_living_space = LivingSpace(room)
                if new_living_space:
                    self.all_rooms.append(new_living_space)
                else:
                    return False
        return True

    def print_room(self, room_name):
        my_room = [room for room in dojo.all_rooms if room.room_name == room_name]
        occupants = my_room.occupants
        if len(occupants) < 1:
            print("Room has no occupants")
            return
        else:
            print("All people in room %s" % room_name)
            print("----------------------------------")
            for occupant in occupants:
                print(occupant.person_name)

    def add_person(self, person_name, person_type, wants_accomodation="N"):
        if person_type == "Staff":
            new_person = Staff(person_name, dojo.all_rooms)
            self.all_people.append(new_person)
            return
        else:
            if wants_accomodation == "Y":
                opt_in = True
            else:
                opt_in = False

            new_person = Fellow(person_name, opt_in, dojo.all_rooms)
            self.all_people.append(new_person)
            return

dojo = Dojo()
dojo.create_room("office", "Purple", "Black", "Brown")
dojo.create_room("living space", "Yellow", "Orange", "Pink")
dojo.add_person("Neil Armstrong", "Staff")
dojo.add_person("Johnson Jones", "Fellow", "Y")

print(len(dojo.all_people))

# print(dojo.all_rooms[0].room_name)
# print(len(dojo.all_rooms))
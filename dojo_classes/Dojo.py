import os
import string
import sys
from subprocess import call
from prettytable import PrettyTable
from dojo_classes.DojoDb import DojoDb
from dojo_classes.Person import *


class Dojo:
    def __init__(self):
        self.dojo_name = "Kenya Dojo"
        self.all_rooms = []
        self.all_people = []

    # Checks whether the room_name you're trying to register is already existent
    def room_already_registered(self, room_name):
        if self.get_room(room_name):
            return True
        else:
            return False

    # Creates a new room of either type Office, or LivingSpace basing on the room_type argument
    def create_room(self, room_type, *room_name):
        result = []
        room_type = room_type.lower()
        if isinstance(room_name, tuple):
            rooms_list = list(room_name)
            # Handle arguments passed from docopt. Get the arguments list
            if not isinstance(rooms_list[0], str):  # pragma: no cover
                rooms_list = rooms_list[0]

        for room in rooms_list:
            room_name = room.strip()
            # Don't create room with invalid chars since the room name is to be used as a PRI. KEY
            if self.invalid_chars(room_name):
                print("Error! The room name contains some invalid characters!")
                continue

            if self.room_already_registered(room_name):
                print("Error! The room %s already exists in the Dojo!" % room_name)
                continue

            if room_type == "office":
                new_office = Office(room_name, 6)
                print("An Office called %s has been successfully created!" % room_name)
                self.all_rooms.append(new_office)
                result.append(new_office)
            elif room_type == "living_space":
                new_living_space = LivingSpace(room, 4)
                print("A Living Space called %s has been successfully created!" % room_name)
                self.all_rooms.append(new_living_space)
                result.append(new_living_space)
            else:
                print("Invalid room type!!")

        return result

    def generate_id(self, obj_type, prefix, counted=0):
        if not counted:
            counted = len([staff for staff in self.all_people if isinstance(staff, obj_type)])

        new_id = prefix + str(counted + 1)

        if new_id not in [person.person_id for person in self.all_people]:
            return new_id

        return self.generate_id(obj_type, prefix, counted)

    def add_person(self, person_name, person_type, wants_accommodation="N"):
        person_type = person_type.lower()
        person_name = person_name.strip()
        # Get boolean equivalents of the passed arguments
        opt_in = False
        if wants_accommodation.lower() == "y":
            opt_in = True

        if self.invalid_chars(person_name):
            print("Error! The person's name contains invalid characters. Try again!")
            return None

        if person_type == "staff":
            if opt_in:
                print("Warning! Staff members can't be allocated living space!")

            new_id = self.generate_id(Staff, "ST")
            new_person = Staff(person_name, new_id)
            print("Staff %s has been successfully added." % person_name)
            new_person.allocate_office(new_person.person_name, self.all_rooms)
            # Add the created person object to the list all_people of Dojo
            self.all_people.append(new_person)
            return new_person
        elif person_type == "fellow":
            new_id = self.generate_id(Fellow, "FW")
            new_person = Fellow(person_name, opt_in, new_id)
            print("Fellow %s has been successfully added." % person_name)
            new_person.allocate_office(new_person.person_name, self.all_rooms)
            # Allocate a living space if fellow chose to opt in
            if opt_in:
                new_person.allocate_living_space(new_person.person_name, self.all_rooms)

            # Add the created person object to the list all_people of Dojo
            self.all_people.append(new_person)
            return new_person
        else:
            print("Invalid person type")
        return None

    def print_room(self, room_name):
        if self.room_already_registered(room_name):
            # Get room object with the particular room name
            my_room = self.get_room(room_name)
            occupants = my_room.occupants
        else:
            print("The room %s does not exist in the Dojo!" % room_name)
            return False

        if not occupants:
            print("\n Room %s has no occupants" % room_name)
            return False
        else:
            print("\n Occupants in room %s" % room_name)
            my_table = PrettyTable(['Person ID', 'Name', 'Person Type'])
            for occupant in occupants:
                if isinstance(occupant, Staff):
                    person_type = "Staff"
                else:
                    person_type = "Fellow"

                my_table.add_row([occupant.person_id, occupant.person_name, person_type])
            print(my_table)
        return True

    def get_room(self, room_name):
        room = [room for room in self.all_rooms if room.room_name == room_name]
        if room:
            return room[0]
        else:
            return None

    def print_allocations(self, file_name=None):
        if not self.all_rooms:
            print("No rooms registered")
            return False
        else:
            for my_room in self.all_rooms:
                print()
                print(my_room.room_name.upper())
                print("-".ljust(31, '-'))
                occupants = []
                for occupant in my_room.occupants:
                    occupants.append(occupant.person_name)
                print(', '.join(occupants))

        # Create a txt file if the filename argument is passed
        if file_name:
            my_file = open("ExternalData/" + file_name + ".txt", "w")
            for my_room in self.all_rooms:
                my_file.write("\n")
                my_file.write(my_room.room_name.upper())
                my_file.write("\n" + "-".ljust(31, '-') + "\n")
                occupants = []
                for occupant in my_room.occupants:
                    occupants.append(occupant.person_name)
                my_file.write(', '.join(occupants) + "\n")
            my_file.close()

    def print_unallocated(self, file_name=None):
        allocated_staff = []
        allocated_fellow_office = []
        allocated_fellow_living_space = []

        for room in self.all_rooms:
            allocated_staff += [occupant for occupant in room.occupants
                                if isinstance(occupant, Staff)]
            allocated_fellow_office += [occupant for occupant in room.occupants
                                        if isinstance(occupant, Fellow) and isinstance(room, Office)]
            allocated_fellow_living_space += [occupant for occupant in room.occupants
                                              if isinstance(occupant, Fellow) and isinstance(room, LivingSpace)
                                              and occupant.opt_in is True]
        unallocated_staff = list(set([person for person in self.all_people if isinstance(person, Staff)])
                                 - set(allocated_staff))
        unallocated_fellow_office = list(set([person for person in self.all_people if isinstance(person, Fellow)])
                                         - set(allocated_fellow_office))
        unallocated_fellow_living_space = list(set([person for person in self.all_people
                                                   if isinstance(person, Fellow) and person.opt_in is True])
                                               - set(allocated_fellow_living_space))
        print("\nUnallocated staff members")
        print("-".ljust(31, '-'))
        print(', '.join(self.print_person_list(unallocated_staff)))

        print("\nFellows without Office Space")
        print("-".ljust(31, '-'))
        print(', '.join(self.print_person_list(unallocated_fellow_office)))

        print("\nFellows without Living Space")
        print("-".ljust(31, '-'))
        print(', '.join(self.print_person_list(unallocated_fellow_living_space)))

        # Create a txt file if filename argument is passed
        if file_name:
            my_file = open("ExternalData/" + file_name + ".txt", "w")
            my_file.write("Unallocated staff members")
            my_file.write("\n" + "-".ljust(31, '-') + "\n")
            my_file.write(', '.join(self.print_person_list(unallocated_staff)))
            my_file.write("\n\n")

            my_file.write("Fellows without Office Space")
            my_file.write("\n" + "-".ljust(31, '-') + "\n")
            my_file.write(', '.join(self.print_person_list(unallocated_fellow_office)))
            my_file.write("\n\n")

            my_file.write("Fellows without Living Space")
            my_file.write("\n" + "-".ljust(31, '-') + "\n")
            my_file.write(', '.join(self.print_person_list(unallocated_fellow_living_space)))
            my_file.write("\n\n")
            my_file.close()

        return [len(unallocated_staff), len(unallocated_fellow_office), len(unallocated_fellow_living_space)]

    def get_person_by_id(self, person_identifier):
        person = [person for person in self.all_people if person.person_id == person_identifier]
        if person:
            return person[0]
        else:
            return None

    def get_person_by_name(self, person_name):
        person = [person for person in self.all_people if person.person_name == person_name]
        if person:
            return person[0]
        else:
            return None

    def reallocate_person(self, person_identifier, room_name):
        new_room = self.get_room(room_name)
        if not new_room:
            print("The room {0} does not exist in the Dojo.".format(room_name))
            return

        # Get the person object based on the person identifier
        person = self.get_person_by_id(person_identifier)
        if not person:
            print("Person {0} does not exist in the Dojo.".format(person_identifier))
            return

        if isinstance(person, Staff) and isinstance(new_room, LivingSpace):
            print("A staff member can't be allocated a living space!")
            return

        # Allocate person to the new room if there is space
        if not len(new_room.occupants) < int(new_room.max_occupants):
            print("Destination room is fully occupied!")
            return

        # Get the room object where the person was assigned previously and remove him
        prev_room = [room for room in self.all_rooms
                     if isinstance(room, type(new_room)) and person in room.occupants]
        if prev_room:
            prev_room = prev_room[0]
            if not isinstance(new_room, type(prev_room)):
                print("{0} can't be reallocated from {1} to {2}. Try again!".
                      format(person.person_name, prev_room.__class__.__name__, new_room.__class__.__name__))
                return
            if new_room is prev_room:
                print("{0} is already an occupant of {1} {2}".
                      format(person.person_name, new_room.__class__.__name__, room_name))
                return
            prev_room.occupants.remove(person)
            new_room.occupants.append(person)
            print("%s has been successfully allocated to %s %s" %
                  (person.person_name, new_room.__class__.__name__, new_room.room_name))
        else:
            print("%s doesn't belong to any %s yet." % (person.person_name, new_room.__class__.__name__))

    def load_people(self):
        file = open("ExternalData/person_data.txt")
        for line in file:
            line.strip()
            data_row = line.split()
            last_param = data_row[-1]
            person_name = ' '.join(data_row[0:2])
            if len(last_param) == 1:
                wants_accommodation = data_row[-1]
                person_type = data_row[-2]
            else:
                wants_accommodation = "F"
                person_type = data_row[-1]
            self.add_person(person_name, person_type, wants_accommodation)
        file.close()

    def print_pretty_allocations(self):
        for room in self.all_rooms:
            self.print_room(room.room_name)

    def print_all_data(self):  # pragma: no cover
        print("Dojo Data")
        my_table = PrettyTable(['Person ID', 'Name', 'Office', 'Living Space'])
        for person in self.all_people:
            person_id = person.person_id
            person_name = person.person_name
            _office = [room for room in self.all_rooms
                       if isinstance(room, Office) and person in room.occupants]
            if _office:
                office = ''.join(_office[0].room_name)
            else:
                office = ''
            _living = [room for room in self.all_rooms
                       if isinstance(room, LivingSpace) and person in room.occupants]
            if _living:
                living_space = ''.join(_living[0].room_name)
            else:
                living_space = ''
            my_table.add_row([person_id, person_name, office, living_space])
        print(my_table)

        print("Registered rooms in the dojo")
        my_table = PrettyTable(['Room Name', 'Room Type'])
        for room in self.all_rooms:
            room_name = room.room_name
            if isinstance(room, Office):
                room_type = "Office"
            else:
                room_type = "Living Space"
            my_table.add_row([room_name, room_type])
        print(my_table)
        return True

    def save_state(self, db_name):
        dojo_db = DojoDb(self)
        dojo_db.save_state(db_name)

    def load_state(self, db_name):
        dojo_db = DojoDb(self)
        dojo_db.load_state(db_name)

    @staticmethod
    def print_person_list(my_list):
        if not my_list:
            print("No data to display")
            return []

        result = []
        for person in my_list:
            result += [person.person_name]
        return result

    # This function is for opening files across multiple platforms
    @staticmethod
    def open_file(file_name):
        if sys.platform == "win32":
            os.startfile(file_name)
        else:
            var = "open" if sys.platform == "darwin" else "xdg-open"
            call([var, file_name])

    @staticmethod
    def invalid_chars(my_string):
        # Populate a list of invalid special characters
        _chars = set(string.punctuation.replace("_", ""))
        if any(char in _chars for char in my_string):
            return True
        else:
            return False

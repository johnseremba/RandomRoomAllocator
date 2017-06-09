from Person import *
from prettytable import PrettyTable
import sqlite3
import string
import os
import sys
import subprocess


class Dojo:
    def __init__(self):
        self.dojo_name = "Kenya Dojo"
        self.all_rooms = []
        self.all_people = []

    # Checks whether the room_name you're trying to register is already existent
    def room_already_registered(self, room_name):
        available = [room for room in self.all_rooms if room.room_name == room_name]
        if len(available) > 0:
            return True
        else:
            return False

    # Creates a new room of either type Office, or LivingSpace basing on the room_type argument
    def create_room(self, room_type, *room_name):
        result = []
        room_type = room_type.lower()
        if type(room_name) == tuple:
            rooms_list = list(room_name)
            # Handle arguments passed from docopt. Get the arguments list
            if not isinstance(rooms_list[0], str):
                rooms_list = rooms_list[0]

        # Populate a list of invalid special characters
        invalid_chars = set(string.punctuation.replace("_", ""))
        for room in rooms_list:
            room_name = room.strip()
            # Don't create room with invalid chars since the room name is to be used as a PRI. KEY
            if any(char in invalid_chars for char in room_name):
                print("Error! The room name contains some invalid characters!")
                continue
            else:
                if not self.room_already_registered(room_name):
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
                else:
                    print("Error! The room %s already exists in the Dojo!" % room_name)
                    continue
        return result

    def add_person(self, person_name, person_type, wants_accommodation="N"):
        person_type = person_type.lower()
        person_name = person_name.strip()

        if person_type == "staff":
            # Generate unique ID for staff member with a prefix ST
            for j in range(len([x for x in self.all_people if isinstance(x, Staff)]), 500):
                new_id = "ST" + str(j + 1)
                if new_id not in [person.person_id for person in self.all_people]:
                    break

            new_person = Staff(person_name, new_id)
            print("Staff %s has been successfully added." % person_name)
            new_person.allocate_office(new_person.person_name, self.all_rooms)

            # Add the created person object to the list all_people of Dojo
            self.all_people.append(new_person)
            return new_person
        elif person_type == "fellow":
            # Get boolean equivalents of the passed arguments
            if wants_accommodation.lower() == "y":
                opt_in = True
            else:
                opt_in = False

            # Generate a uique ID for fellow with a prefix FW
            for j in range(len([x for x in self.all_people if isinstance(x, Fellow)]), 500):
                new_id = "FW" + str(j + 1)
                if new_id not in [person.person_id for person in self.all_people]:
                    break
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
        return

    def print_room(self, room_name):
        if self.room_already_registered(room_name):
            # Get room object with the particular room name
            my_room = [room for room in self.all_rooms if room.room_name == room_name][0]
            occupants = my_room.occupants
        else:
            print("The room %s does not exist in the Dojo!" % room_name)
            return False

        if len(occupants) < 1:
            print("Room %s has no occupants" % room_name)
            return False
        else:
            print("Occupants in room %s" % room_name)
            my_table = PrettyTable(['Person ID', 'Name', 'Person Type'])
            for occupant in occupants:
                if isinstance(occupant, Staff):
                    person_type = "Staff"
                else:
                    person_type = "Fellow"

                my_table.add_row([occupant.person_id, occupant.person_name, person_type])
            print(my_table)
        return True

    def print_allocations(self, file_name):
        if len(self.all_rooms) < 1:
            print("No rooms registered")
            return
        else:
            for my_room in self.all_rooms:
                print()
                print(my_room.room_name.upper())
                print("------------------------------")
                occupants = []
                for occupant in my_room.occupants:
                    occupants.append(occupant.person_name)
                print(', '.join(occupants))

        # Create a txt file if the filename argument is passed
        if file_name is not None:
            my_file = open("ExternalData/" + file_name + ".txt", "w")
            for my_room in self.all_rooms:
                my_file.write("\n")
                my_file.write(my_room.room_name.upper())
                my_file.write("\n------------------------------\n")
                occupants = []
                for occupant in my_room.occupants:
                    occupants.append(occupant.person_name)
                my_file.write(', '.join(occupants) + "\n")
            my_file.close()
            # Open the file with the default application
            self.open_file("ExternalData/" + file_name + ".txt")

    def print_unallocated(self, file_name):
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

        print()
        print("Unallocated staff members")
        print("-------------------------")
        print(', '.join(self.print_person_list(unallocated_staff)))

        print()
        print("Fellows without Office Space")
        print("-------------------------")
        print(', '.join(self.print_person_list(unallocated_fellow_office)))

        print()
        print("Fellows without Living Space")
        print("-------------------------")
        print(', '.join(self.print_person_list(unallocated_fellow_living_space)))

        # Create a txt file if filename argument is passed
        if file_name is not None:
            my_file = open("ExternalData/" + file_name + ".txt", "w")
            my_file.write("Unallocated staff members")
            my_file.write("\n-----------------------------------\n")
            my_file.write(', '.join(self.print_person_list(unallocated_staff)))
            my_file.write("\n")

            my_file.write("Fellows without Office Space")
            my_file.write("\n-----------------------------------\n")
            my_file.write(', '.join(self.print_person_list(unallocated_fellow_office)))
            my_file.write("\n")

            my_file.write("Fellows without Living Space")
            my_file.write("\n-----------------------------------\n")
            my_file.write(', '.join(self.print_person_list(unallocated_fellow_living_space)))
            my_file.write("\n")
            my_file.close()

            # Open the file with the default application
            self.open_file("ExternalData/" + file_name + ".txt")
        return [len(unallocated_staff), len(unallocated_fellow_office), len(unallocated_fellow_living_space)]

    @staticmethod
    def print_person_list(my_list):
        result = []
        for person in my_list:
            result += [person.person_name]
        return result

    def reallocate_person(self, person_identifier, room_name):
        # Get the room object based on the room name
        new_room = [room for room in self.all_rooms if room.room_name == room_name]
        if len(new_room) > 0:
            new_room = [room for room in self.all_rooms if room.room_name == room_name][0]
        else:
            print("The room {0} does not exist in the Dojo.".format(room_name))
            return

        # Get the person object based on the person name
        person = [person for person in self.all_people if person.person_id == person_identifier]
        if len(person) > 0:
            person = [person for person in self.all_people if person.person_id == person_identifier][0]
        else:
            print("Person {0} does not exist in the Dojo.".format(person_identifier))
            return

        # Allocate person to the new room if there is space
        if len(new_room.occupants) < int(new_room.max_occupants):
            # Get the room object where the person was assigned previously and remove him
            prev_room_office = [room for room in self.all_rooms if isinstance(room, Office) and (person in room.occupants)]
            # prev_room_living = [room for room in self.all_rooms if isinstance(room, LivingSpace) and (person in room.occupants)]

            if len(prev_room_office) > 0:
                if new_room == prev_room_office:
                    return
                prev_room = prev_room_office[0]
                prev_room.occupants.remove(person)
                new_room.occupants.append(person)
            # elif len(prev_room_living) > 0:
            #     if new_room == prev_room_living:
            #         return
            #     prev_room = prev_room_living[0]
            #     prev_room.occupants.remove(person)
            #     new_room.occupants.append(person)
            print("%s has been successfully allocated to %s" % (person.person_name, new_room.room_name))
        else:
            print("Destination room is fully occupied!")
            return

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

    def save_state(self, db_name):
        if db_name is not None:
            conn = sqlite3.connect("ExternalData/" + db_name + ".db")
        else:
            conn = sqlite3.connect('ExternalData/dojo.db')
        c = conn.cursor()

        # Create Person Table
        c.execute('''CREATE TABLE IF NOT EXISTS person
        (person_id TEXT PRIMARY KEY NOT NULL,
        person_name TEXT NOT NULL,
        person_type TEXT NOT NULL,
        opt_int INT     
        )''')

        # Create room Table
        c.execute('''CREATE TABLE IF NOT EXISTS room
                (room_name TEXT PRIMARY KEY NOT NULL,
                room_type TEXT NOT NULL,
                max_occupants TEXT NOT NULL
                )''')

        # Create Occupant Table
        c.execute('''CREATE TABLE IF NOT EXISTS occupant
                (person_id TEXT NOT NULL,
                room_name TEXT NOT NULL   
                )''')

        # Save Persons Data
        for person in self.all_people:
            opt_in = 0
            if isinstance(person, Staff):
                person_type = "staff"
            else:
                person_type = "fellow"
                opt_in = int(person.opt_in)
            data_list = [person.person_id, person.person_name, person_type, opt_in]
            c.execute('INSERT OR REPLACE INTO person VALUES (?, ?, ?, ?)', data_list)

        # Save Room Data
        c.execute('DELETE FROM occupant')
        for room in self.all_rooms:
            if isinstance(room, Office):
                room_type = "office"
            else:
                room_type = "living_space"
            data_list = [room.room_name, room_type, room.max_occupants]
            c.execute('INSERT OR REPLACE INTO room VALUES (?, ?, ?)', data_list)
            # Save Occupants Data
            for occupant in room.occupants:
                data_list = [occupant.person_id, room.room_name]
                c.execute('INSERT INTO occupant VALUES (?, ?)', data_list)

        conn.commit()
        print("Data saved successfully")
        conn.close()

    def load_state(self, db_name):
        try:
            conn = sqlite3.connect("ExternalData/" + db_name + ".db")
            c = conn.cursor()

            # Load People
            c.execute('''SELECT * FROM person''')
            people = c.fetchall()
            for person in people:
                person_id = person[0]
                person_name = person[1]
                person_type = person[2]
                opt_in = bool(person[3])
                if person_type == "staff":
                    new_person = Staff(person_name, person_id)
                    self.all_people.append(new_person)
                elif person_type == "fellow":
                    new_person = Fellow(person_name, opt_in, person_id)
                    self.all_people.append(new_person)
                else:
                    print("Invalid person type")
        except sqlite3.OperationalError:
            print("Invalid database name!")

        # Load Rooms
        c.execute('''SELECT * FROM room''')
        rooms = c.fetchall()
        for room in rooms:
            room_name = room[0]
            room_type = room[1]
            max_occupants = room[2]

            if room_type == "office":
                new_room = Office(room_name, max_occupants)
                self.all_rooms.append(new_room)
            elif room_type == "living_space":
                new_room = LivingSpace(room_name, max_occupants)
                self.all_rooms.append(new_room)
            else:
                print("Invalid room type")

            # Load room occupants
            c.execute('SELECT * FROM occupant WHERE room_name=?', [room_name])
            my_occupants = c.fetchall()
            for occupant in my_occupants:
                person_id = occupant[0]
                person = [person for person in self.all_people if person.person_id == person_id][0]
                new_room.occupants.append(person)
        print("Data loaded successfully")
        conn.close()

    def print_pretty_allocations(self):
        for room in self.all_rooms:
            self.print_room(room.room_name)

    def print_all_data(self):
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

    # Got this function from stack overflow, for opening files across multiple platforms
    @staticmethod
    def open_file(filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

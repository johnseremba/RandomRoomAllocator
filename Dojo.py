from RandomRoomAllocator.Room import *
from RandomRoomAllocator.Person import *
import sqlite3

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

    def add_person(self, person_name, person_type, wants_accommodation="N"):
        person_type = person_type.lower()
        if person_type == "staff":
            for j in range(len([x for x in dojo.all_people if isinstance(x, Staff)]), 500):
                new_id = "ST" + str(j + 1)
                if new_id not in [person.person_id for person in dojo.all_people]:
                    break
            new_person = Staff(person_name, dojo.all_rooms, new_id)
            new_person.allocate_office(new_person.person_name, dojo.all_rooms)
            self.all_people.append(new_person)
            return
        elif person_type == "fellow":
            if wants_accommodation == "Y":
                opt_in = True
            else:
                opt_in = False
            for j in range(len([x for x in dojo.all_people if isinstance(x, Fellow)]), 500):
                new_id = "FW" + str(j + 1)
                if new_id not in [person.person_id for person in dojo.all_people]:
                    break
            new_person = Fellow(person_name, opt_in, dojo.all_rooms, new_id)
            new_person.allocate_office(new_person.person_name, dojo.all_rooms)
            if opt_in:
                new_person.allocate_living_space(new_person.person_name, dojo.all_rooms)
            self.all_people.append(new_person)
            return
        else:
            print("Invalid person type")

    def print_room(self, room_name):
        my_room = [room for room in self.all_rooms if room.room_name == room_name][0]
        print(my_room.room_name)
        occupants = my_room.occupants
        if len(occupants) < 1:
            print("Room has no occupants")
            return
        else:
            print("All people in room %s" % room_name)
            print("----------------------------------")
            for occupant in occupants:
                print(occupant.person_name)

    def print_allocations(self):
        if len(self.all_rooms) < 1:
            print("No rooms registered")
            return
        else:
            for my_room in self.all_rooms:
                print("-------------------")
                print(my_room.room_name)
                print("-------------------")
                for occupant in my_room.occupants:
                    print(occupant.person_name)

    def print_unallocated(self):
        allocated_staff = []
        allocated_fellow_office = []
        allocated_fellow_living_space = []
        for room in dojo.all_rooms:
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
        print("Unallocated staff members")
        print("-------------------------")
        self.print_person_list(unallocated_staff)

        print("Fellows without Office Space")
        print("-------------------------")
        self.print_person_list(unallocated_fellow_office)

        print("Fellows without Living Space")
        print("-------------------------")
        self.print_person_list(unallocated_fellow_living_space)

    @staticmethod
    def print_person_list(my_list):
        for person in my_list:
            print(person.person_name)

    def reallocate_person(self, person_identifier, room_name):
        try:
            new_room = [room for room in self.all_rooms if room.room_name == room_name][0]
            person = [person for person in self.all_people if person.person_id == person_identifier][0]
            prev_room = [room for room in self.all_rooms if isinstance(room, Office) and (person in room.occupants)][0]

            if new_room.max_occupants < len(new_room.occupants):
                new_room.occupants.append(person)
                prev_room.occupants.remove(person)
            else:
                print("Destination room is fully occupied!")
        except:
            print("Error! Person or Room not found!")

    def load_people(self):
        my_file = open("person_data.txt")
        line = my_file.readline()
        while line:
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
            line = my_file.readline()
        my_file.close()

    def save_state(self):
        conn = sqlite3.connect('dojo.db')
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

    def load_state(self):
        conn = sqlite3.connect('dojo.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM person''')
        people = c.fetchall()
        for person in people:
            row = list(person)
            # print(person.person_id, person.person_name)
            print(person[0], person[1], person[2], bool(person[3]))

        # cur.execute('''SELECT * FROM tabla1''')
        # todo = cur.fetchall()
        # print
        # todo
        # print
        # len(todo)
        # for i in range(len(todo)):

        print("Data loaded successfully")
        conn.close()

dojo = Dojo()
dojo.load_state()
# dojo.create_room("office", "Purple", "Black", "Brown")
# dojo.create_room("living space", "Yellow", "Orange", "Pink")
# dojo.add_person("Neil Armstrong", "Staff")
# dojo.add_person("Neilee Armstrong", "Staff")
# dojo.add_person("Neilxx Armstrong", "Fellow")
# dojo.add_person("Neilww Armstrong", "Staff")
# dojo.add_person("Johnson Jones", "Fellow", "Y")
# # dojo.load_people()
# print(len(dojo.all_people))
#
# for person in dojo.all_people:
#     print(person.person_id, person.person_name)
# for room in dojo.all_rooms:
#     print(room.room_name, len(room.occupants))
# dojo.print_allocations()
# dojo.print_unallocated()
# dojo.print_room("Purple")
# dojo.save_state()

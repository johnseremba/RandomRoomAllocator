import sqlite3
from dojo_classes.Person import Staff, Fellow
from dojo_classes.Room import LivingSpace, Office


class DojoDb:
    def __init__(self, dojo):
        self.dojo_obj = dojo

    def save_state(self, db_name="dojo"):
        conn = sqlite3.connect("ExternalData/" + db_name + ".db")
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
        for person in self.dojo_obj.all_people:
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
        for room in self.dojo_obj.all_rooms:
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
        print("Data saved successfully in %s.db" % db_name)
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
                    self.dojo_obj.all_people.append(new_person)
                elif person_type == "fellow":
                    new_person = Fellow(person_name, opt_in, person_id)
                    self.dojo_obj.all_people.append(new_person)
        except sqlite3.OperationalError:
            print("Database %s.db doesn't exist!" % db_name)
            return

        # Load Rooms
        c.execute('''SELECT * FROM room''')
        rooms = c.fetchall()
        for room in rooms:
            room_name = room[0]
            room_type = room[1]
            max_occupants = room[2]

            if room_type == "office":
                new_room = Office(room_name, max_occupants)
                self.dojo_obj.all_rooms.append(new_room)
            elif room_type == "living_space":
                new_room = LivingSpace(room_name, max_occupants)
                self.dojo_obj.all_rooms.append(new_room)

            # Load room occupants
            c.execute('SELECT * FROM occupant WHERE room_name=?', [room_name])
            my_occupants = c.fetchall()
            for occupant in my_occupants:
                person_id = occupant[0]
                person = [person for person in self.dojo_obj.all_people if person.person_id == person_id][0]
                new_room.occupants.append(person)
        print("Data loaded successfully")
        conn.close()

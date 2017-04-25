class Room:
    occupants = []
    def __init__(self, room_name):
        self.room_name = room_name
        self.room_id = 0
        self.max_occupants = 0

class Office(Room):
    def __init__(self, room_name):
        self.room_name = room_name
        self.max_occupants = 6
        print("An office called %s has been successfully created!" % self.room_name)


class LivingSpace(Room):
    def __init__(self, room_name):
        self.room_name = room_name
        self.max_occupants = 4
        print("A Living Space called %s has been successfully created!" % self.room_name)
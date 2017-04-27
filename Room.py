class Room:

    def __init__(self, room_name):
        self.room_name = room_name
        self.room_id = 0
        self.max_occupants = 0


class Office(Room):
    def __init__(self, room_name, max_occupants):
        self.room_name = room_name
        self.max_occupants = max_occupants
        self.occupants = []


class LivingSpace(Room):
    def __init__(self, room_name, max_occupants):
        self.room_name = room_name
        self.max_occupants = max_occupants
        self.occupants = []

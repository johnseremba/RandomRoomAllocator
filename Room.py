class Room:
    def __init__(self, room_name):
        self.room_name = room_name
        self.room_id = 0
        self.max_occupants = 0
        self.occupants = []

class Office(Room):
    def __init__(self, room_name):
        super(self, Room).room_name = room_name
        print("Created an office %s" % room_name)

class LivingSpace(Room):
    def __init__(self, room_name):
        super(self, Room).roomname = room_name
        print("Created a living space %s " % room_name)

class Room:
    def __init__(self, room_name, max_occupants):
        self.room_name = room_name
        self.max_occupants = max_occupants
        self.occupants = []
        pass


class Office(Room):
    def __init__(self, room_name, max_occupants):
        super().__init__(room_name, max_occupants)


class LivingSpace(Room):
    def __init__(self, room_name, max_occupants):
        super().__init__(room_name, max_occupants)

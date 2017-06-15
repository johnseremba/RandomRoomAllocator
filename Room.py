class Room:
    def __init__(self, room_name, max_occupants):
        if isinstance(self, Room):
            raise NotImplementedError("You can't directly instantiate a Room object")
        self.room_name = room_name
        self.occupants = []


class Office(Room):
    def __init__(self, room_name, max_occupants):
        super().__init__(room_name, max_occupants)
        self.max_occupants = max_occupants


class LivingSpace(Room):
    def __init__(self, room_name, max_occupants):
        super().__init__(room_name, max_occupants)
        self.max_occupants = max_occupants

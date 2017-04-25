dojo = Dojo()
dojo.create_room("office", "Purple", "Black", "Brown")
dojo.create_room("office", "Yellow", "Orange", "Pink")
dojo.add_person("Neil Armstrong", "Staff")

print(dojo.all_rooms[0].room_name)
print(len(dojo.all_rooms))

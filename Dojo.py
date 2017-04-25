"""Greeter.

Usage:
 Dojo.py create_room <room_type> <room_name> ...
 Dojo.py (-h | --help)

Options:
 -h --help     Show this screen.

"""
import docopt


class Dojo:
    def __init__(self):
        self.dojo_name = "Kenya Dojo"
        self.all_rooms = []
        self.all_people = []


    def create_room(self, room_type, room_name):
        if room_type == "office":
            return Office()

if __name__ == '__main__':
   arguments = docopt(__doc__)
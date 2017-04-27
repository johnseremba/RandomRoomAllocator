"""
This system will be used to automatically allocate spaces to fellow and staff members at random.
Usage:
    main.py create_room <room_type> <room_name> ...
    main.py add_person <first_name> <last_name> <person_type> [<wants_accommodation>]
    main.py print_room <room_name>
    main.py print_allocations [<filename>]
    main.py reallocate_person <person_identifier> <new_room_name>
    main.py print_pretty_allocations
    main.py load_people
    main.py save_state [<database_name>]
    main.py load_state <sqlite_database>
    main.py print_all_data
    main.py
    main.py (-h | --help | --version)

Options:
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from Dojo import Dojo

dojo = Dojo()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Main (cmd.Cmd):
    intro = 'Welcome to the random room allocator!' \
        + ' (type help for a list of commands.)'
    prompt = '(Dojo) '
    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name> ..."""
        room_type = arg['<room_type>']
        room_name = arg['<room_name>']
        dojo.create_room(room_type, room_name)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <last_name> <person_type> [<wants_accommodation>]"""
        first_name = arg['<first_name>']
        last_name = arg['<last_name>']
        person_type = arg['<person_type>']
        person_name = first_name + " " + last_name
        wants_accommodation = arg['<wants_accommodation>']

        if wants_accommodation is None:
            wants_accommodation = "N"
        dojo.add_person(person_name, person_type, wants_accommodation)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>'].strip()
        dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [<filename>]"""
        file_name = arg['<filename>']
        dojo.print_allocations(file_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [<filename>]"""
        file_name = arg['<filename>']
        dojo.print_unallocated(file_name)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person_id = arg['<person_identifier>']
        room_name = arg['<new_room_name>']
        dojo.reallocate_person(person_id, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        dojo.load_people()

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [<database_name>]"""
        db_name = arg['<database_name>']
        dojo.save_state(db_name)

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        db_name = arg['<sqlite_database>']
        dojo.load_state(db_name)

    @docopt_cmd
    def do_print_pretty_allocations(self, arg):
        """Usage: print_pretty_allocations"""
        dojo.print_pretty_allocations()

    @docopt_cmd
    def do_print_all_data(self, arg):
        """Usage: print_all_data"""
        dojo.print_all_data()

    def do_quit(self, arg):
        """Quits out the Random room allocator."""
        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

Main().cmdloop()

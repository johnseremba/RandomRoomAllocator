[![Build Status](https://travis-ci.org/SerryJohns/RandomRoomAllocator.svg?branch=master)](https://travis-ci.org/SerryJohns/RandomRoomAllocator)
[![Coverage Status](https://coveralls.io/repos/github/SerryJohns/RandomRoomAllocator/badge.svg?branch=master)](https://coveralls.io/github/SerryJohns/RandomRoomAllocator?branch=master)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# RandomRoomAllocator
Implementation of a system that randomises allocation of rooms to new Andela Fellows and Staff Members at the Dojo.

## Features
* Create rooms, which can be of type Office or Living Space
* Add Persons to the Dojo. The people can be Fellows or Staff members
* Randomly allocate offices to staff and fellows. Randomly allocate living spaces to fellows that choose to opt in.
* Load People from a txt file directly into the system.
* Print Allocations of fellows and staff in the various rooms.
* Load state from a previously saved database
* Save all data you've worked on during a particular session.

## Installation
```sh
$ git clone https://github.com/SerryJohns/RandomRoomAllocator.git
$ cd your-dir
$ rm -rf .git
``` 
## Commands, their usage and examples

### create_room
This command is responsible for creating offices and living_spaces in the Dojo. You can create as many offices/living_spaces as you want.
Usage: 
```
create_room <room_type> <room_name> ...
Example: create_room office Blue Black
```
### add_person
This command is responsible for creating a person, and automatically assigning office space of living space to them.
Usage: 
```
add_person <first_name> <last_name> <staff | fellow> [<wants_accommodation>]
Example: add_person John Serry staff
         add_person Jackson Brown fellow Y
```

### print_room
This command prints all the people allocated to a particular room.
Usage: 
```
print_room <room_name>
Example: print_room Blue
```

### print_allocations
This command prints all fellow & staff allocations in all registered rooms. Providing an optional file name outputs the result to a text file with the filename provided.
Usage: 
```
print_allocations [<filename>]
Example: print_allocations Blue
```

### reallocate_person
This command reallocates a person to the new room specified. However, this command takes in the person's ID inorder to be able to reallocate them.
Usage: 
```
reallocate_person <person_identifier> <new_room_name>
Example: reallocate_person ST01 Black
```

### print_allocations
This prints all the room allocations in the Dojo. Providing an optional filename parameter outputs the results to a txt file.
Usage: 
```
print_allocations [<filename>]
Example: print_allocations my_file_name.txt
```

### print_pretty_allocations
This prints all the room allocations in a neat format using the prettytable module
Usage: 
```
print_pretty_allocations
```

### load_people
This command loads people from default txt file which can be found in ``` ExternalData/person_data.txt ```
Usage: 
``` load_people ```

### save_state
This saves the data in the current sessions to a datatabase_name
Usage: 
```
save_state [<database_name>]
Example: save_state mydata
```

### load_state
This loads data from a previously created database, or saved session.
Usage: 
``` load_state <sqlite_database>
Example: load_state mydata
```
### print_data
This prints all the data in the database
Usage: 
```
print_all_data
```
## Tests

Enables you to run tests on the different parts of the application to ensure that they are running as intended.

### Running tests
Open the terminal and type in the command below to run tests on the program.
Please remember to use the correct python installation on your system. Replace with ```python3``` if need be.
```
python3 -m unittest discover tests
```

### Gather test coverage data
Determine the percentage of code tested.

```
coverage run -m unittest discover -s tests
```
### Print / Output test coverage report

#### Command-line report
Use the commands below to print out a simple command-line report

```
coverage report -m
```

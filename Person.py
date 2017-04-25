class Person:
    def __init__(self, person_name):
        self.person_name = person_name

    def allocate_office(self):


class Staff(Person):
    def __init__(self, person_name):
        self.person_name = person_name

class Fellow:
    def __init__(self, person_name):
        self.person_name = person_name
        self.allocate_office()

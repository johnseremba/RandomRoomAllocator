class Person:
    def __init__(self, person_name):
        self.person_name = person_name

class Staff(Person):
    def __init__(self, person_name):
        super(self, Person).person_name = person_name

class Fellow:
    def __init__(self, person_name):
        super(self, Person).person_name = person_name

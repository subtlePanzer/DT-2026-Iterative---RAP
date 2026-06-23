class Person:
        db_id: int

        def __init__(self, pid: int):
                self.db_id = pid

        @staticmethod
        def get_person_by_id(pid: int) -> Person:
                return Person(pid) # TODO

class User(Person):
        pass

class Manager(Person):
        pass

class Admin(Person):
        pass

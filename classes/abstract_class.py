from abc import ABCMeta, abstractmethod

class Animal(metaclass=ABCMeta):
    PLANET = 'Earth'

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    @abstractmethod
    def say_hello(self): pass

class Dog(Animal):

    def __init__(self, name, race):
        super().__init__(name)
        self.race = race

    def pee(self):
        print("I pee like dog.")

    def __str__(self):
        return "{0} {1}".format(super().__str__(), self.race)

    def say_hello(self):
        print("Hello like a dog.")

tommy = Dog('Tommy', 'Rhodesian ridgeback')
tommy.pee()
print(tommy)


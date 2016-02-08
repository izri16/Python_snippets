from abc import ABCMeta, abstractmethod

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

class Fruit(metaclass=ABCMeta):
    
    def __init__(self, country):
        self.country = country

    @abstractmethod
    def __str__(self):
        pass


class Banana(Fruit):

    def __str__(self):
        return "Banana from {0}".format(self.country)

class Apple(Fruit):

    def __str__(self):
        return "Apple from {0}".format(self.country)

@singleton
class FruitFactory:
    '''
    Singleton factory class for Fruits instances. Only one
    instance for every fruit type may exists (supplier).
    '''
    instances = {}
    fruit_objects = {'banana': Banana, 'apple': Apple}

    def create_fruit(self, fruit, country):
        if (not fruit in self.fruit_objects.keys()):
            raise Exception('No such fruit.')
    
        if (not fruit in self.instances.keys()):
            self.instances[fruit] = self.fruit_objects[fruit](country)
        return self.instances[fruit]


factory = FruitFactory()
sk = factory.create_fruit('banana', 'sk')
cz = factory.create_fruit('apple', 'cz')
uk = factory.create_fruit('banana', 'uk')

print(sk)
print(cz)
print(uk)


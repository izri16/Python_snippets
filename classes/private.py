class Dog:
   
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

tom = Dog('Tom')
print(tom.get_name())

# Will throw an Error
# print(tom.__name)

print(tom._Dog__name)


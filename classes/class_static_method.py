'''
Static method is like function. Do not take
self so can't access object attributes.
'''

class Dog:

    @staticmethod
    def bark():
        print("Haf haf.")

Dog.bark()


'''
When decorate with classmethod we get class object
instead of instance.
'''

class Hero:
    
    @classmethod
    def have_a_break(cls):
        if (cls.__name__ == 'GoodHero'):
            print("No break! You need to save the world. Take snickers.")
        else:
            print("Quick rest and then damage, damage, damage")

class GoodHero(Hero):
    pass

class BadHero(Hero):
    pass

class VeryBadHero(BadHero):
    pass

spiderman = GoodHero()
sauron = BadHero()
saurons_wife = VeryBadHero()

spiderman.have_a_break()
sauron.have_a_break()
saurons_wife.have_a_break()


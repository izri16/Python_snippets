'''
Use 'in' to check if key exists in dictonary.

Mutable object can not be used as keys.
'''

my_dict = {}
my_dict['name'] = 'Richard'
del my_dict['name']
del my_dict

my_dict = {'name':'Richard', 'age':21, 2:1234}

# when the keys are strings
my_dict = dict(name='Richard', age=21) 

# when keys are arbitrary
my_dict = dict([('name', 'Richard'),('age',21),(2,1234)])

print(my_dict.items())
print(my_dict.keys())
print(my_dict.values())

my_dict_copy = my_dict.copy()
my_dict.clear()

'''
Dictonary comprehension.
'''
my_dict = {x: x**2 for x in (2,4,6)}


'''
Usefull applications.
'''

array = [1,4,7,2,8,9,5,4,4,7]

'''
Check if there are two same items in array in expected time O(n).
'''

hash_set = {}
for item in array:
    if (item in hash_set):
        print("same")
        break
    else:
        hash_set[item] = 1

'''
Check if there are arbitrary many same items in array.
'''
hash_set = {}
count = 3
for item in array:
    if (item in hash_set):
        if (hash_set[item] >= count - 1):
            print("same")
            break
        else:
            hash_set[item] += 1
    else:
        hash_set[item] = 1


'''
For every item in array find how many times it appears in O(n).
'''

stats = {}
for item in array:
    if (item in stats):
        stats[item] += 1
    else:
        stats[item] = 1

print(stats)


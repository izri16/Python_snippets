# two ways to create set
s1 = {1,1,3,1,3,5,2,1,4}
s2 = set([7,1,5,4,1,1,2,7,5,4])

'''
Basic methods.
'''

s1.update({100,200,300})
s1.add(100)

# throw exception if not exists
s1.remove(1)

# do not throw exception if not exists
s1.discard(1)

# remove and return arbitrary element
s1.pop()

# remove all items
s1.clear()

'''
Set operations.
'''

a = set('aabsdebbffdc0551200')
b = set('abdfewfabc07ex')
print(a)
print(b)

print(a - b)
print(b - a)

# union
print(a | b)

# intersection
print(a & b)

# in a or b but not in both (symetric difference)
print(a ^ b)    

'''
Set comprehension.
'''

a = {x for x in 'abracadabra' if x not in 'abc'}


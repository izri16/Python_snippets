'''
Basics.
'''

l1 = [1,2,3,4,5]

print(l1[-2])
print(l1[1:3])
print(l1[2:])

print(max(l1))
print(min(l1))
print(len(l1))

del l1[2:4]
print(l1)
del l1

print([1,2,3] + [4,5,6])
print([1,2,3] * 6)

'''
Usefull lists methods.
cmp() does not exists in Python3.
'''
l1 = list((1,2,3))
l1 = [1,2,3]

l1.append(5)
print(l1)

l1.insert(3, 4)
print(l1)

l1.remove(2)
print(l1)

l1.pop()
print(l1)

l1.pop(0)
print(l1)

print(l1.index(3))
print(l1.count(3))

l1.sort()
print(l1)

l1.sort(reverse=True)
print(l1)

l1.reverse()
print(l1)

l2 = l1.copy()
print(l2)

l1.clear()
print(l1, l2)

l1.extend(l2)
print(l1)

'''
Stack.
'''

stack = [3,4,5]
stack.append(6)
stack.append(7)
stack.pop()

'''
Queues. 
Using lists as queues is slow because of insert to begining.
Use deque collection.
'''

from collections import deque

queue = deque([1,2,3])
queue.append(4)
print(queue)
print(queue.popleft())

'''
Deque.
Elements can be added or removed from both ends.
May be implemented using circular buffer.
'''

from collections import deque

queue = deque([1,2,3])
queue.append(4)
print(queue)
print(queue.popleft())
queue.appendleft(5)
print(queue)
print(queue.pop())

'''
List comprehension.
'''

squares = [i**2 for i in range(10)]
print(squares)

mess = [(i*j, min(i,j)) for i in range(10) for j in range(10) if i != j]
print(mess)

matrix = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]
]

transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)


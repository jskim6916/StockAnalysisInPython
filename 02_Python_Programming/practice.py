myTuple = ('a', 'b', 'c', [10,20,30], abs, max)
print(myTuple[3])
print(myTuple[4](-100))
print(myTuple[5](myTuple[3]))

help('keywords')

max = 3
print(max)
print(max([3,2]))

import keyword
keyword.__file__
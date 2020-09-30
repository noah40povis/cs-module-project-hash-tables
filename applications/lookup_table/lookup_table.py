# Your code here
import math 
import random

def slowfun_too_slow(x, y):
    v = math.pow(x, y) #x raised to the power y
    v = math.factorial(v) #gets the factorial of 5
    v //= (x + y) # 
    v %= 982451653

    return v

lookup_table = {}

def slowfun(x, y):
    #if x and y are not in the lookup table which is a cache
    if (x, y) not in lookup_table:
        #run slowfun_too_slow on the new x,y , but set it equal to lookup table 
        lookup_table[(x,y)] = slowfun_too_slow(x,y)
      #return lookup_table   
    return lookup_table[(x,y)]




# Do not modify below this line!

for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')

# see http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#testing-for-truth-values

import random

###TASK: if Boolean

has_money = random.choice([False, True])
print('has_money', has_money)

if has_money:   ###PLACEHOLDER: has_money --> has_money == True
    print("Nice guy..")
else:  # if not has_money
    print("Poor guy..")


###TASK: if String

name = random.choice(["Tom", "", None])
print( name, repr(name) )

if not name:    ###PLACEHOLDER: not name --> name == "" or name == None
    name = "Anonymous"

print("Hello, %s!" % name)


###TASK: if Number

money = random.choice([100, -10, 0])
print('money', money)

if  money:  ###PLACEHOLDER: money -->  money != 0
    print("We have + or - (positive or negative amount of money)")


###TASK: if container (list, tuple, dict, set)

data = random.choice( [  
            [10, 5, 3], 
            [],
            [1]
        ] )
print("data", data)


if data: ###PLACEHOLDER: data -->  len(data) > 0
    print( "Average is", sum(data)/len(data) )
    

import random

###TASK Data printing
name = "Tom"
age = 21
money = random.randint( 0, 100 )

print( name, "is", age, "years old." ) ###PLACEHOLDER: name --> ???
print( "%s is %s years old." % (name, age) ) ###PLACEHOLDER: age --> ???
print( "%s has %s euros." % (name, money) ) ###PLACEHOLDER: name, money --> ???


###TASK newline magic
# '\n' means newline (it is one of  metacharacters which have special meaning)
print( "\n"*10 ) # print 10 newlines ###PLACEHOLDER: *10 -->  ???



###TASK Variables
money = 6
print("We have ", money, "euros.")

money += 2  # We found 2 euros! ###PLACEHOLDER: + --> ..add..
print( "Now it's %s euros." % money )

pica = 5  ###PLACEHOLDER: pica --> ??
money -= pica # buy a pica ###PLACEHOLDER: money --> ??
print("Pica was tasty. It costed %s euros, so %s left.." % (pica, money) )


###TASK chained conditions (if/else/elif)
# let's say we have some money
money = random.randint( 0, 10 )

# and we are hungry
# and pica costs 5eu, beer -- 3eu
if money >= 8:      ###PLACEHOLDER  if --> ?
    print( "We can buy pica and beer" )
elif money >= 5: 
    print( "We can buy pica (without beer)" )
elif money >= 3:    ###PLACEHOLDER  elif --> ?
    print( "We can buy beer (without pica)" )
else:   ###PLACEHOLDER  else --> ?
    print( "let's go for a walk.." )

###TASK Lists
food = [ 'bread', 'meat', 'water', 'apples' ]
food.append('cheese') # add one more item

n = len(food)  # how many items do we have

if 'bread' in food and 'cheese' in food:
    print( "We could make a sandwich" )

if 'oranges' not in food:
    print( "No oranges for today" )

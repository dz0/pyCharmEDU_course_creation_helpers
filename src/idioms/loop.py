# List loops
finances = [10, -5, 15]

###TASK: foreach with numeration
for i, x in enumerate(finances): #use i, x in ...  ###PLACEHOLDER: i, x in enumerate(finances) --> i in range(len(finances))
    print( "On day", i+1, "our finances were", x ) ###PLACEHOLDER: x --> finances[i]


###TASK: last element
last_day = finances[ -1 ] ###PLACEHOLDER: -1 -->  len(finances) - 1
print( "last_day", last_day )

###TASK: sum
total = sum( finances )  ###PLACEHOLDER: sum( finances ) --> 0; for x in finances: total += x
print( "total", total )

###TASK: list comprehension: construct new list - modify elements
double = [x*2 for x in finances]  ###PLACEHOLDER:  [x*2 for x in finances] --> []; for x in finances: double.append( x*2 )
print( "double", double )


###TASK: list comprehension: filter positives
###GROUP_LINES
profits = [x for x in finances if x > 0]   ###PLACEHOLDER: [x for x in finances if x > 0] -->
###[]
###for x in finances:
###    if x > 0:
###        profits.append( x )
###GROUP_LINES_END        

print( "profits", profits )

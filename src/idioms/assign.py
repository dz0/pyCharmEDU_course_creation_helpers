# example
foo = 10

###TASK: assign multiple / tuplex
# let x be 2   and    y be 5
x, y = 2, 5 ###PLACEHOLDER: 2, 5 --> ???
print(x, y)

# make a 20  and    b 10
b, a = 10, 20 ###PLACEHOLDER: b, a -->  ??
print(a, b)

###TASK: swap
a = 10
b = 12
a, b = b, a ###PLACEHOLDER: a, b = b, a --> tmp = a; a=b; b = tmp

print(a, b)


###TASK: unpack (py3)
x, *etc = 10, 20, 30, 40 ###PLACEHOLDER: *etc --> ????
print(x, etc)


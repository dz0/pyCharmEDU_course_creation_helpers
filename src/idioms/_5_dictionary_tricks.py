# Dictionary loops
prices = {'bread': 2, 'water':1, 'beer':2.5, 'apples':0.6 }

print( "goods:", list( prices.keys() ) )

average = sum(prices.values()) / len( prices)  
print( "average price:", average)


###TASK: get value or None
if random.choice([True, False]):
    del prices['beer']

###GROUP_LINES
beer_price = prices.get('beer') ) ###PLACEHOLDER:  --> 
###if 'beer' in prices:
###    beer_price = prices['beer'] 
###else:
###    beer_price = None
###GROUP_LINES_END

print(beer_price)




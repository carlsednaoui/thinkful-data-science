the_count = [1, 2, 3, 4, 5]
fruits = ['apples', 'oranges', 'pears', 'apricots']
change = [1, 'pennies', 2, 'dimes', 3, 'quarters']

for number in the_count:
	print(f"This is count {number}.")

for fruit in fruits:
	print(f"This is a fruitype of: {fruit}.")

for i in change:
    print(f"I got {i}")

elements = []

# for i in range(0,6):
# 	print(f"Adding {i} to the list.")
# 	elements.append(i)

elements = range(0, 6)

for i in elements:
	print(f"Printing element {i}.")
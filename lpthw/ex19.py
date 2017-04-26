def cheese_and_crackers(cheese_count, boxes_of_crackers):
	print(f"You have {cheese_count} cheeses!")
	print(f"You have {boxes_of_crackers} boxes of crackers.")
	print("Man, that's enough for a party.")
	print("Get a blanket.\n")

print("We can just give the fn numbers directly:")
cheese_and_crackers(20, 30)

print("OR, we can use variables:")
amount_of_cheese = 100
amount_of_crackers = 5000

cheese_and_crackers(amount_of_cheese, amount_of_crackers)

print("We can do math too.")
cheese_and_crackers(10 + 20, 5 + 6)

print("And we can combine it all:")
cheese_and_crackers(amount_of_cheese + 100, amount_of_crackers + 10000)
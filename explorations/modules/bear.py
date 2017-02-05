class Bear(object):
	def __init__(self, name, fav_food, age):
		self.name = name
		self.fav_food = fav_food
		self.age = age

	def birthday(self):
		self.age += 1

	def __repr__(self):
		return "The bear's name is {} and it is {} years old".format(self.name, self.age)
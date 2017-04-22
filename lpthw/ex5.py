name = 'Zed A. Shaw'
age = 35 # not a lie
height = 74 # inches
weight = 180 # lbs
eyes = 'Blue'
teeth = 'White'
hair = 'Brown'

print(f"Let's talk about {name}.")
print(f"He's {height} inches tall.")
print(f"He's {weight} pounds heavy.")
print("Actually that's not too heavy.")
print(f"He's got {eyes} eyes and {hair} hair.")
print(f"His teeth are usually {teeth} depending on the coffee.")

# this line is tricky, try to get it exactly right
total = age + height + weight
print(f"If I add {age}, {height}, and {weight} I get {total}.")

print("If I add {}, {}, and {} I get {}.".format(age, height, weight, total))

inch_to_centimeter = 2.54
pound_to_kilogram = 0.453592

height_in_centimeters = height * inch_to_centimeter
weight_to_kilogram = weight * pound_to_kilogram

print(f"In pound I weight {weight} but in kg I weight {weight_to_kilogram}")
print(f"Im {height} in inches but in cm I am {height_in_centimeters}")
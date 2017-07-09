# create a mapping of state to abbreviation
states = {
    'Oregon': 'OR',
    'Florida': 'FL',
    'California': 'CA',
    'New York': 'NY',
    'Michigan': 'MI'
}

# create a basic set of states and some cities in them
cities = {
    'CA': 'San Francisco',
    'MI': 'Detroit',
    'FL': 'Jacksonville'
}

# add some more cities
cities['NY'] = 'New York'
cities['OR'] = 'Portland'

for state, abbrev in list(states.items()):
	print(f"{state} is abbreviated {abbrev}")

# safely get a abbreviation by state that might not be there
state = states.get('Texas')

if not state:
    print("Sorry, no Texas.")

city = cities.get('TX', 'Does Not Exist')
print(f"The city for the state 'TX' is: {city}")

print("*" * 10)
for state, abbrev in states.items():
    print(f"{state} is abbreviated {abbrev}")
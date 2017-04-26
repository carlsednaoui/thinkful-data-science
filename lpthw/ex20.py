from sys import argv

script, input_file = argv

def print_all(f):
	print(f.read())

def rewind(f):
	f.seek(0)

def print_a_line(line_count, f):
	print(line_count, f.readline())

# file:///Users/carl/sites/thinkful-data-science/lpthw/offline/website/learnpythonthehardway.org/python3/ex20.html
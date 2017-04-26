from sys import argv

script, filename = argv

print(f"We're going to erase {filename}.")
print(f"Here's the content of {filename}")

file = open(filename)
print(f"""
===
{file.read()}
===
""")
file.close()

print("Quit now if you want to. Hit return to continue.")

input("?")

print("Opening the file...")
target = open(filename, 'w')

print("Truncating the file. Goodbye!")
target.truncate()

print("Now let's add some content.")

line1 = input("Line 1: ")
line2 = input("Line 2: ")
line3 = input("Line 3: ")

print("I'm going to write these to the file.")

target.write(f"""{line1}
{line2}
{line3}
""")

print("And finally, we close it.")
target.close()
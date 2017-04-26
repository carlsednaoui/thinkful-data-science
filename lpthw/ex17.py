from sys import argv
from os.path import exists

script, from_file, to_file = argv

print(f"Copying from {from_file} to {to_file}.")

indata = open(from_file).read()
open(to_file, 'w').write(indata)

print("All done.")
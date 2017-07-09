i = 0
numbers = []

def do_loop(u):
    global i
    while i < u:
        print(f"At the top i is {i}")
        numbers.append(i)

        i += 1
        print("Numbers now: ", numbers)
        print(f"At the bottom i is {i}")


do_loop(int(input("Until when to loop? \n> ")))

print("The numbers: ")

for num in numbers:
    print(num)

# module name = same as python file
# class name = the actual class name
# from bear import Bear

# to use this with the __init__.py file, you need to have
# from .bear import Bear
# OR
from module_exploration.bear import Bear

jack = Bear("jack", "apples", 3)

print(jack.age)
jack.birthday()
print("It was Jack's birthday")
print(jack.age)

# to run this do
# $ python -m forest

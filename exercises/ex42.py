class Animal(object):
    pass

# Dog is-a Animal object
class Dog(Animal):

    def __init__(self, name):
        # Dog has a name
        self.name = name

# Cat is-a Animal
class Cat(Animal):

    def __init__(self, name):
        # Cat has a name
        self.name = name

# Person is-a object
class Person(object):

    def __init__(self, name):
        # Person has-a name
        self.name = name

        # Person has-a pet of some kind
        self.pet = None


# Employee is-a Person
class Employee(Person):

    def __init__(self, name, salary):
        # superclass helps call Employee class here
        super(Employee, self).__init__(name)
        # Employee has-a salary
        self.salary = salary

# Fish is-a object
class Fish(object):
    pass

# Salmon is-a Fish
class Salmon(Fish):
    pass

# Halibut is-a Fish:

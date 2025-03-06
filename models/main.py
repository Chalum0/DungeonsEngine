import random

def main(entity):
    print("hello world")
    entity.pos = (random.randint(-2, 2), random.randint(-2, 2), random.randint(-2, 2))

def greetings():
    print("hi")
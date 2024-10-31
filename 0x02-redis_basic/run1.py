#!/usr/bin/env python3
from functools import wraps

def my_deco(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(args, kwargs)
        print(args[0].a)
        return f(*args, **kwargs)
    return wrapper

@my_deco
def example(arg1, arg2):
    """Doc"""
    print("Called")

class C:
    def __init__(self):
        self.a = 1
    @my_deco
    def func(self):
        print("Self, Here")   

c = C()

c.func()
#!/usr/bin/env python3
"""
Main File to Test Code Runs
"""
from typing import Callable
import redis
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ system to count how many times methods of
    the Cache class are called."""
    @wraps(method)
    def inc_count(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return inc_count


class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: str | bytes | int | float) -> str:
        key = uuid4()
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable):
        val = self.get(key)

        if not val:
            return "(nil)"

        return fn(val)

    def get_str(self, key: str):
        val = self.get(key)

        if not val:
            return "(nil)"

        return val.decode("utf-8")

    def get_int(self, key: str):
        val = self.get(key)

        if not val:
            return "(nil)"

        return int(val)

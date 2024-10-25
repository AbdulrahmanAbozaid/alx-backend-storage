#!/usr/bin/env python3
"""
Module for interacting with Redis for basic caching operations.
This module implements a Cache class with several methods to store,
retrieve, count calls, and maintain a history of function inputs and
outputs using Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method of the Cache class is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and
    outputs for a particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with input-output history tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)

        return output
    return wrapper


class Cache:
    """
    Cache class for storing data in Redis and
    performing various caching operations.
    """

    def __init__(self):
        """
        Initialize the Redis client and flush any existing data.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the provided data in Redis with a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated key where the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieve data from Redis and apply an optional conversion function.

        Args:
            key (str): The key where data is stored in Redis.
            fn (Optional[Callable]): A function to
            apply to the data upon retrieval.

        Returns:
            The data retrieved from Redis, optionally converted.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve string data from Redis.

        Args:
            key (str): The key where string data is stored in Redis.

        Returns:
            str: The data retrieved from Redis as a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve integer data from Redis.

        Args:
            key (str): The key where integer data is stored in Redis.

        Returns:
            int: The data retrieved from Redis as an integer.
        """
        return self.get(key, fn=int)


def replay(method: Callable):
    """
    Display the history of calls for a particular method in the Cache class.

    Args:
        method (Callable): The method to replay call history for.
    """
    self = method.__self__
    method_name = method.__qualname__

    call_count = int(self._redis.get(method_name) or 0)
    print(f"{method_name} was called {call_count} times:")

    inputs = self._redis.lrange(f"{method_name}:inputs", 0, -1)
    outputs = self._redis.lrange(f"{method_name}:outputs", 0, -1)

    for input_val, output_val in zip(inputs, outputs):
        input_val = input_val.decode("utf-8")
        output_val = output_val.decode("utf-8")
        print(f"{method_name}(*{input_val}) -> {output_val}")

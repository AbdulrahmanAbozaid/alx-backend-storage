#!/usr/bin/env python3
"""
This module provides a function for fetching a
web page, caching it in Redis for
10 seconds, and tracking the number of times each URL is accessed.
"""

import requests
import redis
from typing import Callable

# Initialize Redis client
cache = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator that tracks how many times a URL is accessed.
    Args:
        method (Callable): The function to be decorated.
    Returns:
        Callable: The wrapped function with counting behavior.
    """
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cache.incr(count_key)  # Increment the access count for the URL
        return method(url)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL, caches it for
    10 seconds, and returns the content.
    Args:
        url (str): The URL of the web page to fetch.
    Returns:
        str: The HTML content of the web page.
    """
    cache_key = f"cached:{url}"
    cached_content = cache.get(cache_key)

    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch fresh content if not in cache
    response = requests.get(url)
    content = response.text

    # Cache the content with an expiration of 10 seconds
    cache.setex(cache_key, 10, content)
    return content

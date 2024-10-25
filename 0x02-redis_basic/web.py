#!/usr/bin/env python3
"""
Module for implementing a simple web page caching and access tracking system
using Redis. The module fetches the content of a web page, caches it for 10
seconds, and keeps track of how many times the page has been accessed.
"""

import requests
import redis
from typing import Callable

# Initialize Redis client
cache = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator to count accesses to a specific URL using Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with access counting functionality.
    """
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cache.incr(count_key)  # Increment the access count for the URL
        return method(url)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL, cache it for 10 seconds, and track the
    number of accesses.

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


if __name__ == "__main__":
    # Test URL to simulate a slow response and test caching
    test_url = "http://slowwly.robertomurray.co.uk/delay" +\
            "/3000/url/https://www.example.com"

    print(get_page(test_url))  # First request - caches the page content
    print(get_page(test_url))  # Second request - should retrieve from cache

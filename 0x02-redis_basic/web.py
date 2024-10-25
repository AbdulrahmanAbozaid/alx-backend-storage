#!/usr/bin/env python3
"""Module to implement a web cache with expiration in
Redis and track URL access count."""

import requests
import redis

# Initialize Redis client
r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the content of a URL, caches it with a
    10-second expiration, and increments
    the access count each time the URL is requested.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the web page.
    """
    # Define separate Redis keys for caching content and tracking access count
    cache_key = f"cached:{url}"  # Key for cached content
    count_key = f"count:{url}"   # Key to track number of accesses

    # Check if the content is already cached
    cached_content = r.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch fresh content if not cached
    response = requests.get(url)
    content = response.text

    # Store content in cache with 10 seconds expiration
    r.setex(cache_key, 10, content)

    # Increment the access count for the URL
    r.incr(count_key)

    return content

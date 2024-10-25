#!/usr/bin/env python3
"""Module to implement a web cache with expiration in Redis."""
import requests
import redis


r = redis.Redis()


def get_page(url: str) -> str:
    """Fetch URL content and cache with expiration."""
    cache_key = f"count:{url}"
    cached_content = r.get(url)

    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    content = response.text

    r.incr(cache_key)
    r.setex(url, 10, content)  # Cache content with 10 seconds expiration

    return content

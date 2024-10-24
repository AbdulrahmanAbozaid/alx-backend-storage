#!/usr/bin/env python3
"""
Module to update topics of a school document based on the school name
"""

def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.
    
    :param mongo_collection: The collection to perform the update.
    :param name: The school name to search for.
    :param topics: List of topics to be updated.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )

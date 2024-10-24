#!/usr/bin/env python3
"""
Module to return the list of schools having a specific topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic.
    
    :param mongo_collection: The collection to query from.
    :param topic: The topic to search for.
    :return: List of schools containing the given topic.
    """
    return mongo_collection.find({"topics": topic})

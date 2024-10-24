#!/usr/bin/env python3
""" Insert a document """
def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document and returns its ID """
    return mongo_collection.insert_one(kwargs).inserted_id

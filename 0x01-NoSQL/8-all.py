#!/usr/bin/env python3
""" List all documents """
def list_all(mongo_collection):
    """ Lists all documents in the collection """
    return list(mongo_collection.find())

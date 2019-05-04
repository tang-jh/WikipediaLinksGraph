"""
Python module for extracting a list of source-target pagelinks to the defined depth 
from a starting list of wikipedia page(s).
When run as a script, a csv of the source-target pagelinks will be saved
Parameters are set from the config.py file
"""
import pymongo
import pandas as pd
import json
from config import *

# set up based on config.py values
mongo = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
client = mongo[DATABASE_NAME]
collection = client[COLLECTION_NAME]
inputlist = INPUTLIST
depth = LINKS_DEPTH

def item_generator(json_input, lookup_key):
    """ Parser for json document """
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

def pagelinks(collection, id):
    """ Returns list of all the links from source page """
    links = []
    document_links = item_generator(collection.find_one({"_id": id}), "links")
    for i in document_links:
        for p in range(len(i)):
            links.append(i[p].get('page'))
    return links

def nextlinks(collection, graphlist, inputlist, cnt):
    """ Returns next level list of pagelinks and a consolidated graphlink list """
    next_links = []
    for i in inputlist:
        for l in pagelinks(collection, i):
            if l not in next_links:
                next_links.append(l)
            graphlist.append([i, l])
            if cnt == 0:
                print('Start page links generation')
            elif (cnt % 10000 == 0) and (cnt != 0):
                print('Processing...: {} pages processed'.format(cnt))
            cnt += 1
    return next_links, cnt
        
def linksgraph(collection, inputlist, depth=1):
    """
    Returns a list of source-target pairs. 
    inputlist must be a list of starting page(s)
    """
    graphlist = []
    d = 1
    cnt = 0
    while d <= depth:
        inputlist, cnt = nextlinks(collection, graphlist, inputlist, cnt)
        d += 1
    print('Done! {} page returned'.format(cnt))
    return graphlist

if __name__ == '__main__':
    outputlist = linksgraph(collection, inputlist, depth)
    pd.DataFrame(outputlist).to_csv(OUTPUT_FILENAME, index=None, header=None)
# WikipediaLinksGraph

## Introduction
The intended usage is to retrieve Wikipedia page links from a given list of starting page(s), traversing to the level of depth defined by the user.

When run as a script, the output is a csv file of source-target pairs, which can be fed into graph analysis tools (e.g. [Gephi](https://gephi.org), [NetworkX](https://networkx.github.io)).

## Prerequisite
Requires a [wikipedia dump](https://dumps.wikimedia.org) to be loaded as a MongoDB collection. This tool, [wikipedia-to-mongodb](https://www.npmjs.com/package/wikipedia-to-mongodb), could be used to help with the import.

### Dependency
- pandas
- pymongo

## How to use
### Running as a Python script
Parameters of the script is set in `config.py`. Below is a list explaining what each variable mean:
- MONGODB_HOST - the host name of your MongoDB instance (str)
- MONGODB_PORT - the port number of your MongoDB instance (int)
- DATABASE_NAME - the name of your database (str)
- COLLECTION_NAME - the name of your collection (str)
- INPUTLIST - a list of the page to start pagelink extraction (list)
- LINKS_DEPTH - distance (geodesic) of travel from the list of starting page(s) (int)
- OUTPUT_FILENAME - path of the output file

To run the script, type the following command into your terminal

```
python wikipagelinks.py
```

### Using as a module
It is probably more useful to use this as part of your Python project. Use the `linksgraph` method to return a list of pagelinks.

```
import pymongo
import wikipagelinks as wpl

mongo = pymongo.MongoClient(host = 'your_host', port = port_num)
client = mongo['your_database_name']
collection = client['your_collection_name']
inputlist = ['Science']

pagelinks = wpl.linksgraph(collection, inputlist, depth=2)

# Downstream processes here
```

The `item_generator` method can be tweaked to extract links from specific sections of a single page. 
First, explore the structure of the page of interest by loading it as a document using the `pymongo` interface.
This will produce a json object, which can be subsetted using the `json` library.
This can in fact be tweaked to extract any document field, since it parses json objects.

```
import pymongo
import json
from pprint import pprint
import wikipagelinks as wpl

mongo = pymongo.MongoClient(host = 'your_host', port = port_num)
client = mongo['your_database_name']
collection = client['your_collection_name']

mypage = collection.find_one({'_id': 'Science'})
pprint(mypage) #Study page structure
# Extracts links at the second paragraph of the page's main text body.
links_from_section = wpl.item_generator(mypage['sections'][1], 'links')
```

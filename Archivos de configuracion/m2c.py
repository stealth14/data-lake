#!usr/bin/python
"""
Sample python script to migrate documents from mongodb to apache couchdb database.
This script reads a document from mongodb and writes it to couchdb database.
**Script does not support the use case for 'documents with attachments'
"""

import json
from argparse import ArgumentParser
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


DB_COUNT, DOCUMENT_COUNT = 0, 0
SKIPPED = []
argp = ArgumentParser()
argp.add_argument("-c", "--couchdb", help="couchdb endpoint, example: http://Vicente:Vicente@localhost:5984 ", required=True)
argp.add_argument("-m", "--mongodb", help="mongodb endpoint, example: mongodb://localhost:27017 ", required=True)
args = argp.parse_args()

# CouchDB REST endpoint. equivalent to http://username:password@localhost:5984. Replace with actual CouchDB endpoint
URL = args.couchdb

# Test CouchDB connection
try:
    response = requests.get(URL)
    if response.status_code == 200:
        print('CouchDB connection: Success')
    if response.status_code == 401:
        print('CouchDB connection: failed', response.json())
except requests.ConnectionError as e:
    raise e

# couchDB connection HEADERS
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# MongoDB connection endpoint using pymongo MongoClient. Replace with actual MongoDB IP or FQDN endpoint
CLIENT = MongoClient(args.mongodb)

# Test MongoDB connection
try:
    CLIENT.admin.command('ismaster')
    print('MongoDB connection: Success')
except ConnectionFailure as cf:
    print('MongoDB connection: failed', cf)

# Database list example in MongoDB. ['admin', 'zzzzz', 'local', 'yyyy', ....]
DBS = ['gamestoplomasesperado']  # for pymongo version > 3.4.0, replace this line with DBS = CLIENT.list_database_names()

# read collections and documents
for db in DBS:
    if db not in ('admin', 'local'):  # omitting  special internal db's, 'admin'(DBS[0]) and 'local'(DBS[2])
        cols = CLIENT[db].collection_names()  # for pymongo > 3.4.0, replace with cols = CLIENT[db].list_collection_names())
        for col in cols:
            print('Querying documents from collection {} in database {}'.format(col, db))
            for x in CLIENT[db][col].find():  # iterate though all records inside a collection
                try:
                    documents = json.dumps(x)
                except TypeError as t:
                    print('current document raised error: {}'.format(t))
                    SKIPPED.append(x)  # creating list of skipped documents for later analysis
                    continue    # continue to next document
                except Exception as e:
                    raise e
                # create database in CouchDB for the first time if it doesn't exist
                try:
                    response = requests.Session().get(URL+'/'+db+'-'+col, auth=('Vicente', 'Vicente'), headers=HEADERS, verify=False)
                    if 'error' in response.json():  # db doesnt exist on destination, create it
                        print('Creating a new database {} in CouchDB'.format(db+'-'+col))
                        output = requests.Session().put(URL+'/'+db+'-'+col, auth=('Vicente', 'Vicente'), headers=HEADERS, verify=False)
                        if output.status_code == 201 or 202:
                            DB_COUNT += 1
                    # insert documents in couchDB database.
                    output = requests.Session().post(URL+'/'+db+'-'+col, auth=('Vicente', 'Vicente'), headers=HEADERS, data=documents, verify=False)
                    if output.status_code == 201 or 202:
                        DOCUMENT_COUNT += 1
                except requests.exceptions.RequestException as e:
                    raise e
print('DB migration summary: {} Databases and {} Documents created in CouchDB'.format(DB_COUNT, DOCUMENT_COUNT))
print('Skipped documents: \n {}'.format(SKIPPED))

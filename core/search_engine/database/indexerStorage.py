from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from numpy.linalg import norm



class InvertedIndexStorage:
    def __init__(self,):
        client = MongoClient('mongodb://localhost:27017/')
        database = client['search_engine']
        self.rev_indexes = database["reverse_index"]
        self._create_index()

    def _create_index(self,):
        try:
            self.rev_indexes.create_index("word")
        except Exception as e:
            print(f"Index might already exist: {e}")    

    def addDocument(self, word, url):
        self.rev_indexes.update_one(
            {'word' : word},
            {'$push' : {'urls' : url}},
            upsert=True
        )

    def getDocuments(self, word):
        doc_list = self.rev_indexes.find_one({'word' : word})
        if doc_list == None:
            return []
        return self.rev_indexes.find_one({'word' : word})['urls']    

class SemanticIndexStorage:
    def __init__(self, ):
        client = MongoClient('mongodb://localhost:27017/')
        database = client['search_engine']
        self.indexes = database["semantic_index"]
        self.createIndex()

    def createIndex(self,):
        try:
            self.indexes.create_index("url")
        except Exception as e:
            print(f"Index might already exist: {e}")
    
    def insertDocument(self, document, url):
        self.indexes.insert_one(document)
    
    def search(self, searchSpace = None):
        if searchSpace == None:
            return list(self.indexes.find({}, {"_id": 1, "url": 1, "embedding": 1}))
        else:
            return list(self.indexes.find({'url' : {'$in' : searchSpace}}))

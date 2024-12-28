from pymongo import MongoClient, UpdateOne, InsertOne
from bson.objectid import ObjectId
from datetime import datetime
import time

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
    
    """
    v1.0
    def addDocument(self, word, url):
        self.rev_indexes.update_one(
            {'word' : word},
            {'$push' : {'urls' : url}},
            upsert=True
        )
    """

    def insertDocuments(self, words, url):
        operations = [InsertOne({'word' : word, 'url' : url, "timestamp": datetime.now()}) for word in words]
        self.rev_indexes.bulk_write(operations)

    def getDocuments(self, word):
        doc_list = list(self.rev_indexes.find({'word' : word}))
        if doc_list == None:
            return []
        return [doc['url'] for doc in doc_list]

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
    
    def insertDocument(self, embedding, url):
        self.indexes.insert_one({'url': url, 'embedding': embedding, "timestamp": datetime.now()})
    
    def search(self, searchSpace = None):
        if searchSpace == None:
            return list(self.indexes.find({}, {"_id": 1, "url": 1, "embedding": 1}))
        else:
            return list(self.indexes.find({'url' : {'$in' : searchSpace}}))

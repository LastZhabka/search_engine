from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from numpy import dot
from numpy.linalg import norm
from datetime import datetime

def get_hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    return sha256.hexdigest()

class URLQueue:
    def __init__(self,):
        client = MongoClient('mongodb://localhost:27017/')
        database = client['search_engine']
        self.unprocessed_urls = database['unprocessed_urls']
        self.unprocessed_urls.create_index('timestamp')
        self.size = self.unprocessed_urls.estimated_document_count()

    def push_url(self, url):
        self.size += 1
        self.unprocessed_urls.insert_one({
            'url':url,
            'timestamp': datetime.now()
        })
    
    def is_empty(self,):
        return (self.size == 0)

    def get_url(self,):
        self.size -= 1
        return self.unprocessed_urls.find_one_and_delete(filter={}) # is it fast?

class Logger:
    def __init__(self,):
        client = MongoClient('mongodb://localhost:27017/')
        self.logger = client['search_engine']['logger']
    
    def add_info(self, text):
        self.logger.insert_one({
            'text' : text
        })

class  URLStorage:
    def __init__(self,):
        client = MongoClient('mongodb://localhost:27017/')
        self.visited_urls = client['search_engine']['visited_urls']
        self.createIndex()

    def createIndex(self,):
        try:
            self.visited_urls.create_index("url")
        except Exception as e:
            print(f"Index might already exist: {e}")

    def add_url(self, url):
        if self.is_visited(url):
            return
        self.visited_urls.insert_one({
            'url': url,
        })

    def is_visited(self, url):
        return (True if self.visited_urls.find_one({"url" : url}) else False)

class URLsGraph:
    def __init__(self,):
        client = MongoClient('mongodb://localhost:27017/')
        self.urls_graph = client['search_engine']['urls_graph']
        self.createIndex()

    def createIndex(self,):
        try:
            self.urls_graph.create_index("url")
        except Exception as e:
            print(f"Index might already exist: {e}")

    def connect_urls(self, url_1, url_2):
        self.urls_graph.update_one(
            {'url' : url_1},
            {'$push' : {'urls' : url_2}},
            upsert=True
        )


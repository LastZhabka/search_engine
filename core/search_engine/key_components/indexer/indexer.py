from sentence_transformers import SentenceTransformer
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.database.indexerStorage import SemanticIndexStorage, InvertedIndexStorage
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import reduce

class Indexer(ABC):
    
    @abstractmethod
    def __init__(self, ):
        pass
    
    @abstractmethod
    def insertDocument(self, document, url):
        pass
    
    @abstractmethod
    def searchDocument(self, documentInfo, searchSpace = None, topK = 50):
        pass

class SemanticIndexer(Indexer):
    def __init__(self,):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.indexStorage = SemanticIndexStorage()
    
    def insertDocument(self, document, url):
        documentEmbeddings = self.model.encode(document)
        self.indexStorage.insertDocument(embedding = documentEmbeddings.tolist(), url=url)

    def searchDocument(self, documentInfo, searchSpace=None, topK = 100):
        queryEmbedding = self.model.encode(documentInfo)[0]
        candidateDocuments = self.indexStorage.search(searchSpace)        
        similarities = [(-1, "") for _ in range(topK)]
        for candidate in candidateDocuments:
            if searchSpace != None and (not candidate['url'] in searchSpace):
                raise RuntimeError("Doc is not in the searchSpace")
            candidateEmbeddings = np.array(candidate["embedding"]) # shape (|Chunks|, 343)
            embSimiliarities = np.dot(candidateEmbeddings, queryEmbedding) / (np.linalg.norm(queryEmbedding) * np.linalg.norm(candidateEmbeddings, axis = 1))
            similarity = np.max(embSimiliarities)
            similarities[0] = (similarity, candidate['url'])
            similarities.sort(key = lambda _ : _[0])
        documents = []
        for score, url in reversed(similarities):
            if score == -1:
                break
            documents.append(url)
        return documents

class WordIndexer(Indexer):
    def __init__(self,):
        self.indexStorage = InvertedIndexStorage()
    
    def buildNGram(self, words, N):            
        return [reduce(lambda x, y: x + "_" + y, words[k + 1 : k + N], words[k]) for k in range(0, len(words) - N + 1)]

    def insertDocument(self, document, url):
        if len(document) == 0:
            return
        self.indexStorage.insertDocuments(document + self.buildNGram(document, 2) + self.buildNGram(document, 3), url)

    def searchDocument(self, documentInfo, searchSpace = None, topK = 50):
        docs = defaultdict(int)        
        for k in range(1, 4):    
            for word in self.buildNGram(documentInfo, k):
                print(word)
                temp = defaultdict(int)
                for doc in self.indexStorage.getDocuments(word):
                    temp[doc] += 1
                    docs[doc] += np.power(2 - k * 0.4, -float(temp[doc]))
        return [item[0] for item in sorted(docs.items(), key = lambda x: x[1], reverse=True)[0:topK]]
    

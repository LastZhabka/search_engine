from sentence_transformers import SentenceTransformer
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.database.indexStorage import SemanticIndexStorage, InvertedIndexStorage
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict, Counter
from functools import reduce

class Indexer(ABC):
    
    @abstractmethod
    def __init__(self, ):
        pass
    
    @abstractmethod
    def insertDocument(self, document, url):
        pass
    
    @abstractmethod
    def searchDocument(self, documentInfo, searchSpace = None, topK = 50, docsCount = 0):
        pass

class SemanticIndexer(Indexer):
    def __init__(self,):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.indexStorage = SemanticIndexStorage()
    
    def insertDocument(self, document, url):
        documentEmbeddings = self.model.encode(document)
        self.indexStorage.insertDocument(embedding = documentEmbeddings.tolist(), url=url, text=document)

    def searchDocument(self, documentInfo, searchSpace=None, topK = 100, docsCount = 0):
        queryEmbedding = self.model.encode(documentInfo)[0]
        candidateDocuments = self.indexStorage.search(searchSpace)        
        similarities = [(-1, "", None, None) for _ in range(topK)]
        for candidate in candidateDocuments:
            if searchSpace != None and (not candidate['url'] in searchSpace):
                raise RuntimeError("Doc is not in the searchSpace")
            candidateEmbeddings = np.array(candidate["embedding"]) # shape (|Chunks|, 343)
            embSimiliarities = np.dot(candidateEmbeddings, queryEmbedding) / (np.linalg.norm(queryEmbedding) * np.linalg.norm(candidateEmbeddings, axis = 1))
            similarity = np.max(embSimiliarities)
            similarities[0] = (similarity, candidate['url'], candidateEmbeddings, candidate["text"])
            similarities.sort(key = lambda _ : _[0])
        urls, embeddings, texts = [], [], []
        for score, url, embedding, text in reversed(similarities):
            if score == -1:
                break
            urls.append(url)
            embeddings.append(embedding)
            texts.append(text)
        return urls, embeddings, texts

class WordIndexer(Indexer):
    def __init__(self,):
        self.indexStorage = InvertedIndexStorage()
    
    def buildNGram(self, words, N):            
        return [reduce(lambda x, y: x + "_" + y, words[k + 1 : k + N], words[k]) for k in range(0, len(words) - N + 1)]

    def insertDocument(self, document, url):
        if len(document) == 0:
            return
        words = Counter(document + self.buildNGram(document, 2) + self.buildNGram(document, 3))
        vocabulary = words.keys()
        self.indexStorage.insertDocuments(words, url)

    def searchDocument(self, documentInfo, searchSpace = None, topK = 50, docsCount = 0):
        docs = defaultdict(int)        
        for k in range(1, 4):
            for word in Counter(self.buildNGram(documentInfo, k)).keys():
                docs_with_word = self.indexStorage.getDocuments(word)
                if len(docs_with_word) == 0:
                    continue
                wordIDF = np.log(docsCount  / (len(docs_with_word) + 0.0))
                for url, frequency in docs_with_word:
                    docs[url] += wordIDF * (1 + np.log(frequency))
                    #docs[url] += 1 - np.power(8.0, -frequency)
        return [item[0] for item in sorted(docs.items(), key = lambda x: x[1], reverse=True)[0:topK]]
    

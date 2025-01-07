"""
THRASH CODE, JUST TESTED ANOTHER PART, IGNORE IT FOR NOW.

"""


"""
DOCUMENT:
(document text)

QUESTION:
(users question)

INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENT text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return {NONE}
"""
from sentence_transformers import SentenceTransformer
import os, sys
sys.path.append(os.getcwd())
from core.search_engine.search_engine import SearchEngine
import numpy as np

def cos(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class RAGPipeline:
    def __init__(self,):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.searchEngine = SearchEngine()

    def ask(self, queryText):
        queryEmbedding = self.model.encode(queryText)
        urls, embeddings, texts = self.searchEngine.get(queryText)
        sources = []
        for url, embedding, text in zip(urls, embeddings, texts):
            for subEmbedding, subText in zip(embedding, text):
                similarity = cos(queryEmbedding, np.array(subEmbedding))
                sources.append((similarity, url, subText))
        #print(sources)
        sources.sort(key = lambda _ : _[0])
        sources = reversed(sources)
        for source in sources:
            print(source[2])


from sentence_transformers import SentenceTransformer
import os, sys
sys.path.append(os.getcwd())
from core.search_engine.search_engine import SearchEngine
from core.rag_pipeline.llm_connector.llm_connector import LLMConnector
import numpy as np
from functools import reduce



def cos(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class RAGPipeline:
    def __init__(self,):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.threshold = 0.5
        self.searchEngine = SearchEngine()
        self.llm_connector = LLMConnector()


    def getBestSubSources(self, sources, queryEmbedding, K = 12):
        result = []
        for url, embedding, text in zip(sources["urls"], sources["vectors"], sources["texts"]):
            for subEmbedding, subText in zip(embedding, text):
                similarity = cos(queryEmbedding, np.array(subEmbedding))
                if similarity > self.threshold:
                    result.append((similarity, url, subText))
        result.sort(key = lambda _ : _[0])
        result.reverse()
        return result[0:K]

    def preparePrompt(self, sources, queryText):
        sourceTexts = [source[2] for source in sources]
        prompt = reduce(lambda a, b: a + "\n" + b, sourceTexts, "DOCUMENT:\n")
        prompt += f"QUESTION:\n{queryText}\n"
        prompt += "INSTRUCTIONS:\nAnswer the users QUESTION using the DOCUMENT text above.\n Keep your answer ground in the facts of the DOCUMENT.\n If the DOCUMENT doesn’t contain the facts to answer the QUESTION return {NONE}"
        return prompt

    def ask(self, queryText):
        queryEmbedding = self.model.encode(queryText)
        bestSources = self.getBestSubSources(sources = self.searchEngine.get(queryText), queryEmbedding = queryEmbedding, K = 12)
        prompt = self.preparePrompt(sources=bestSources, queryText=queryText)
        print(f"QUERY: {queryText}")
        answer = self.llm_connector.complete_text(prompt)
        print("ANSWER:")
        print(answer)
        print("SOURCES:")
        for source in bestSources:
            print(source[1])

                

import sys, os
sys.path.append(os.getcwd())
from core.search_engine.key_components.indexer.indexer import SemanticIndexer, WordIndexer
from core.search_engine.key_components.tokenizer.tokenizer import TextBatchTokenizer, WordTokenizer

import time

class SearchPipeline:
    def __init__(self,):
        self.tokenizers = [WordTokenizer(), TextBatchTokenizer()]
        self.indexers = [WordIndexer(), SemanticIndexer()]

    def searchDocument(self, queryText, topK = 20):
        searchSpace = None
        docsCount = self.indexers[1].indexStorage.getSize()
        for layer in range(2):
            tokens = self.tokenizers[layer].getTokens([queryText])
            searchSpace = self.indexers[layer].searchDocument(tokens, searchSpace, (20 if layer == 1 else 100), docsCount)
        return searchSpace
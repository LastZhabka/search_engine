import sys, os
sys.path.append(os.getcwd())
from core.search_engine.indexing_pipeline.indexer.indexer import SemanticIndexer, WordIndexer
from core.search_engine.indexing_pipeline.tokenizer.tokenizer import TextBatchTokenizer, WordTokenizer
from utilities.TextRetriever import TextRetriever

import time

class IndexingPipeline:
    def __init__(self,):
        self.tokenizers = [WordTokenizer(), TextBatchTokenizer()]
        self.indexers = [WordIndexer(), SemanticIndexer()]
    
    def retrieveText(self, responseContent, format):
        match format:
            case "pdf":
                return TextRetriever.retrievePDFText(responseContent)
            case "html":
                return TextRetriever.retrieveHTMLText(responseContent)
        raise RuntimeError("Wrong format in Indexing Pipeline")

    def indexDocument(self, responseContent, format, url):
        responseText = self.retrieveText(responseContent, format)
        for layer in range(2):
            tokens = self.tokenizers[layer].getTokens(responseText)
            self.indexers[layer].insertDocument(document = tokens, url = url)

    def searchDocument(self, queryText, topK = 20):
        searchSpace = None
        for layer in range(2):
            tokens = self.tokenizers[layer].getTokens([queryText])
            searchSpace = self.indexers[layer].searchDocument(tokens, searchSpace, (2 - layer) * topK)
        return searchSpace
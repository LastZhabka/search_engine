import sys, os
sys.path.append(os.getcwd())
from core.search_engine.crawler.crawler import WebCrawler
from core.search_engine.indexing_pipeline.indexing_pipeline import IndexingPipeline

class SearchEngine:
    def __init__(self,):
        self.indexingPipeline = IndexingPipeline()
        self.crawler = WebCrawler(self.indexingPipeline.indexDocument)
    
    def start_crawling(self,):
        self.crawler.start_crawling()

    def get(self, queryText):
        print(self.indexingPipeline.searchDocument(queryText=queryText, topK=20))


x = SearchEngine()
"""
SearchEngine().start_crawling()
"""
x.get("Data Science Major, DSCT Major requirements")

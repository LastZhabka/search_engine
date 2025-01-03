import sys, os
sys.path.append(os.getcwd())
from core.search_engine.key_components.crawler.crawler import WebCrawler
from core.search_engine.pipelines.indexing_pipeline.indexing_pipeline import IndexingPipeline
from core.search_engine.pipelines.search_pipeline.search_pipeline import SearchPipeline
import asyncio

class SearchEngine:
    def __init__(self,):
        self.indexingPipeline = IndexingPipeline()
        self.searchPipeline = SearchPipeline()
        self.crawler = WebCrawler(self.indexingPipeline.indexDocument)
    
    def start_crawling(self,):
        asyncio.run(self.crawler.start_crawling())

    def get(self, queryText):
        print(self.searchPipeline.searchDocument(queryText=queryText, topK=20))


x = SearchEngine()
x.crawler.urls.add_url("https://prog-crs.hkust.edu.hk/ugprog/2024-25/COMP")
x.crawler.unprocessedURLs.push_url("https://prog-crs.hkust.edu.hk/ugprog/2024-25/COMP")
SearchEngine().start_crawling()
#asyncio.run(x.crawler.crawl_url("http://publications.ust.hk/Annual_Report/2008-2009/annual_report_0809.pdf"))
#SearchEngine().start_crawling()

"""
import time

t0 = time.time()
x.get("ICPC")
print(time.time() - t0)
"""

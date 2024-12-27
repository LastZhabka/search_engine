import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.database.crawlerStorage import URLQueue, URLsGraph, URLStorage, Logger
from utilities.URLProcessor import URLProcessor
import time

class WebCrawler:
    def __init__(self, indexingCallback):
        self.unprocessedURLs = URLQueue()
        self.urlsGraph = URLsGraph()
        self.urls = URLStorage()
        self.logger = Logger()
        self.indexingCallback = indexingCallback

        self.urlProcessor = URLProcessor() # utility

    def propagate_from_url(self, url, links):
        for link in links:
            next_url = self.urlProcessor.joinURLs(url, link.get("href"))
            if len(next_url) > 0:
                self.urlsGraph.connect_urls(next_url, url)
                if self.urls.is_visited(next_url):
                    continue
                self.urls.add_url(next_url)
                self.unprocessedURLs.push_url(next_url)

    def crawl_url(self, url):
        try:
            response = requests.get(url)
        except:
            return
        response_type = self.urlProcessor.getResponseType(response)
        if response_type == 'html' or response_type == 'pdf':
            self.indexingCallback(responseContent=response.content, format=response_type, url=url)
        if response_type == 'html':
            soup = BeautifulSoup(response.content, "html.parser")
            self.propagate_from_url(url, soup.find_all('a'))
        
    def start_crawling(self, ):
        while not self.unprocessedURLs.is_empty():
            url = self.unprocessedURLs.get_url()['url']
            self.crawl_url(url)
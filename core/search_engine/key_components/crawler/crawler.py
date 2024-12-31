import requests
from bs4 import BeautifulSoup
import sys, os
sys.path.append(os.getcwd())
from core.search_engine.database.crawlerStorage import URLQueue, URLsGraph, URLStorage, Logger
from utilities.URLProcessor import URLProcessor
import time
import asyncio
import aiohttp

class WebCrawler:
    def __init__(self, indexingCallback):
        self.unprocessedURLs = URLQueue()
        self.urlsGraph = URLsGraph()
        self.urls = URLStorage()
        self.logger = Logger()
        self.indexingCallback = indexingCallback
        self.debt = 0
        self.urlProcessor = URLProcessor() # utility

    async def propagate_from_url(self, url, links):
        for link in links:
            next_url = self.urlProcessor.joinURLs(url, link.get("href"))
            if len(next_url) > 0:
                self.urlsGraph.connect_urls(next_url, url)
                if self.urls.is_visited(next_url):
                    continue
                self.urls.add_url(next_url)
                self.unprocessedURLs.push_url(next_url)

    async def asyncIndexingCallbackWrapper(self, responseContent, format, url):
        self.indexingCallback(responseContent = responseContent, format = format, url = url)
        self.debt -= 1

    async def crawl_url(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url)
                content = await response.content.read()
        except:
            return
        response_type = self.urlProcessor.getResponseType(response)
        if response_type == 'html' or response_type == 'pdf':
            self.debt += 1
            task = asyncio.create_task(self.asyncIndexingCallbackWrapper(content, response_type, url))
            if response_type == "pdf":
                await task

        if response_type == 'html':
            soup = BeautifulSoup(content, "html.parser")
            await self.propagate_from_url(url, soup.find_all('a'))

        
    async def start_crawling(self, ):
        while not self.unprocessedURLs.is_empty():
            t0 = time.time()
            url = self.unprocessedURLs.get_url()['url']
            await self.crawl_url(url)
            print(f"Crawled url : {url}, {time.time() - t0}, debt : {self.debt}")